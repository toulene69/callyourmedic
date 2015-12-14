from django.shortcuts import render , render_to_response
from django.http import HttpResponse , HttpResponseRedirect , Http404
from django.template.loader import get_template
from django.core.context_processors import csrf
from django.db import IntegrityError, transaction
import traceback
# model imports
from models import WebUser , WebGroup
from organisations.models import Organisation
from hospitals.models import Hospital, Department

# form imports
from forms import PortalUserLoginForm, PortalHospitalCreationForm, PortalHospitalSelectionForm
from addresses.forms import AddressForm

from utils.web_portal_session_utils import isUserLogged , createUserSession , destroyUserSession , userSessionExpired, isUserRequestValid

import logging

logger = logging.getLogger(__name__)

"""Login/Logout"""
def login(request):
    if isUserLogged(request):
        return HttpResponseRedirect('web/dashboard/')
    else:
        error = None
        args = {}
        if request.POST:
            formLogin = PortalUserLoginForm(request.POST)
            if formLogin.is_valid():
                orgIdentifier = formLogin.cleaned_data['org_identifier']
                username = formLogin.cleaned_data['user_name']
                password = formLogin.cleaned_data['password']
                try:
                    organisation = Organisation.objects.get(org_identifier__iexact = orgIdentifier)
                except(KeyError, Organisation.DoesNotExist):
                    error = "Org Identifier incorrect"
                try:
                    user = WebUser.objects.get(usr_email__iexact = username, usr_org= organisation, usr_status = True)
                    #return HttpResponseRedirect('/web/dashboard/')
                    if user.usr_password == password:
                         createUserSession(request,user)
                         return HttpResponseRedirect('/web/dashboard/')
                    else:
                        print "Password incorrect"
                        error = "User or password incorrect"
                except(KeyError, WebUser.DoesNotExist):
                    error = "User does not exists!"
            else:
                error = "Form is not valid"
        else:
            formLogin = PortalUserLoginForm()
            request.session.set_test_cookie()
        if 'sessionError' in request.GET:
			if request.GET['sessionError'] == '100':
				print ('******* Session Expired ***')
				args['sessionError'] = True
        args.update(csrf(request))
        args['formLogin'] = formLogin
        args['error'] = error
        return render_to_response('wlogin.html',args)

def logout(request):
    temp = get_template('wlogout.html')
    destroyUserSession(request)
    html = temp.render()
    return HttpResponse(html)

def dashboard(request):
    # usr_details = {
    #     'first_name' : 'Apoorv',
    #     'group_id' : 1,
    # }
    # return render_to_response('wdashboard.html',usr_details)
    if isUserLogged(request):
        args = {}
        return render(request,'wdashboard.html',args)
    else:
        return userSessionExpired()

""" Org Views for Webportal"""

def org_dashboard(request):
    args = {}
    if isUserLogged(request):
        org_id = int(request.session['org_id'])
        organisation = Organisation.objects.get(org_id__exact = org_id)
        depts = list(Department.objects.filter(department_org__exact = org_id))
        args['org'] = organisation
        args['depts'] = depts
        return render(request,'w_dashboard_org.html',args)
    else:
        return userSessionExpired()

def org_departments(request):
    if isUserLogged(request):
        return render(request,'w_department_org.html')
    else:
        return userSessionExpired()

""" Ends Org Views for webportal"""

""" Hospital Views for webportal """

def hospital_dashboard(request):
    if isUserLogged(request):
        return render(request,'w_dashboard_hospital.html')
    else:
        return userSessionExpired()

def hospital_details(request,org_id=0,hospital_id=0):
    error = None
    args = {}
    if isUserLogged(request):
        if isUserRequestValid(request,org_id):
            if org_id!=0:
                organisation = Organisation.objects.get(org_id__exact = org_id)
                args['org'] = organisation
                if hospital_id !=0 :
                    hospital = Hospital.objects.get(hospital_org__exact = org_id, hospital_id__exact = hospital_id)
                    args['hospital'] = hospital
            else:
                error = 'Invalid request'
            formHospitalChoice = PortalHospitalSelectionForm(org_id)
            args['formHospitalChoice'] = formHospitalChoice
            return render(request,'w_details_hospital.html',args)
        else:
            error = 'Invalid Request'
        args['error'] = error
        return render(request,'w_details_hospital.html',args)
    else:
        return userSessionExpired()


def hospital_new(request,org_id=0):
    error = None
    args = {}
    if isUserLogged(request):
        if isUserRequestValid(request,org_id):
            if request.POST:
                formHospital = PortalHospitalCreationForm(request.POST)
                formAddress = AddressForm(request.POST)
                if formHospital.is_valid() & formAddress.is_valid():
                    organisation = Organisation.objects.get(org_id__exact = org_id)
                    branchCode = formHospital.cleaned_data['hospital_branch_code']
                    hospitalPresent = list(Hospital.objects.filter(hospital_branch_code__iexact = branchCode))
                    if len(hospitalPresent) >0 :
                        error = 'Branch code already exists. Please insert a unique code!'
                    else:
                        try:
                            with transaction.atomic():
                                address = formAddress.save()
                                hospital = formHospital.save(commit=False)
                                hospital.hospital_address = address
                                hospital.hospital_org = organisation
                                hospital.hospital_status = True
                                hospital.save()
                            args['new_hospital_added'] = hospital.hospital_name
                            args['new_hospital_id'] = hospital.hospital_id
                            return render(request,'w_dashboard_hospital.html',args)
                        except:
                            traceback.print_exc()
                            error = 'Error saving new hospital!'
                else:
                    error = 'Error creating new hospital. Form submitted is invalid'
            else:
                formHospital = PortalHospitalCreationForm()
                formAddress = AddressForm()
        else:
            error = 'Invalid request!'
        args.update(csrf(request))
        args['formHospital'] = formHospital
        args['formAddress'] = formAddress
        args['error'] = error
        return render(request,'w_new_hospital.html',args)
    else:
        return userSessionExpired()

""" End Hospital views """

""" User and User Groups """

def usr_dashboard(request):
    if isUserLogged(request):
        return render(request,'w_dashboard_usr.html')
    else:
        return userSessionExpired()

def usr_users(request):
    if isUserLogged(request):
        return render(request,'w_users_usr.html')
    else:
        return userSessionExpired()

def usr_group(request):
    if isUserLogged(request):
        return render(request,'w_group_usr.html')
    else:
        return userSessionExpired()

""" Ends User and User Groups """
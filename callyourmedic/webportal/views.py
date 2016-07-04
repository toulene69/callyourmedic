from django.shortcuts import render , render_to_response
from django.http import HttpResponse , HttpResponseRedirect , Http404
from django.template.loader import get_template
from django.core.context_processors import csrf
from django.db import IntegrityError, transaction
import traceback
# model imports
from models import WebUser , WebGroup
from organisations.models import Organisation, Apikey, OrgSettings
from hospitals.models import Hospital, Department, HospitalSettings
from doctors.models import DoctorDetails, DoctorRegistration, send_mail_to_doctor

# form imports
from forms import PortalUserLoginForm, PortalHospitalCreationForm, PortalHospitalSelectionForm, PortalDoctorDetailsForm, PortalDoctorRegistrationForm, PortalDoctorSelectionForm
from addresses.forms import AddressForm

from utils.web_portal_session_utils import isUserLogged , createUserSession , destroyUserSession , userSessionExpired, isUserRequestValid
from utils.app_utils import generateRandomPassword, generateDoctorCode, checkPassword, getPasswordHash
from utils import app_utils

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
                orgIdentifier = orgIdentifier.strip()
                username = username.strip()
                password = password.strip()
                try:
                    organisation = Organisation.objects.get(org_identifier__iexact = orgIdentifier)
                except(KeyError, Organisation.DoesNotExist):
                    traceback.print_exc()
                    error = "Org Identifier incorrect"
                    formLogin = PortalUserLoginForm()
                    request.session.set_test_cookie()
                    args.update(csrf(request))
                    args['formLogin'] = formLogin
                    args['error'] = error
                    return render_to_response('wlogin.html',args)
                try:
                    user = WebUser.objects.get(usr_email__iexact = username, usr_org= organisation, usr_status = True)
                    #return HttpResponseRedirect('/web/dashboard/')
                    if checkPassword(password,user.usr_password):
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
        if 'setting' in request.GET :
            result = request.GET['setting']
            args['result'] = result
        org_id = int(request.session['org_id'])
        organisation = None
        depts = None
        apikey = None
        try:
            organisation = Organisation.objects.get(org_id__exact = org_id)
            depts = list(Department.objects.filter(department_org__exact = org_id))
            apikey = list(Apikey.objects.filter(apikey_org = org_id))
        except:
            traceback.print_exc()
            args['error'] = "Organisation details could not be found"
            return render(request,'w_dashboard_org.html',args)

        if organisation.org_settings is None:
            args['isSettings'] = False
        else:
            settings = organisation.org_settings
            args['isSettings'] = True
            args['subscription'] = app_utils.get_subscription_type(settings.orgsettings_subscription)
            args['billing_cycle'] = app_utils.get_billing_cycle(settings.orgsettings_billing_cycle)
            args['email']         = settings.orgsettings_email
            args['email_smtp']    = settings.orgsettings_email_smtp
            args['voice_rate']    = settings.orgsettings_voice_rate
            args['video_rate']    = settings.orgsettings_video_rate
            args['subscription_rate'] = settings.orgsettings_subscription_rate
            args['status'] = settings.orgsettings_status
            args['isVoice'] = False
            args['isVideo'] = False
            args['isMarketPlace'] = settings.orgsettings_marketplace
            if organisation.org_settings.orgsettings_subscription == 'C':
                args['isVoice'] = True
            else:
                args['isVoice'] = True
                args['isVideo'] = True
        if len(apikey) == 0:
            args['apikey'] = None
        else:
            args['apikey'] = apikey[0]

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
    hospital = None
    organisation = None
    departments = None
    if isUserLogged(request):
        if 'setting' in request.GET :
            result = request.GET['setting']
            args['result'] = result
        if isUserRequestValid(request,org_id):
            if org_id!=0:
                try:
                    organisation = Organisation.objects.get(org_id__exact = org_id)
                    args['org'] = organisation
                except:
                    error = 'Organisation in request could not be found! Please try again.'
                    args['error'] = error
                    return render(request,'w_details_hospital.html',args)
                if hospital_id !=0 :
                    try:
                        hospital = Hospital.objects.get(hospital_org__exact = org_id, hospital_id__exact = hospital_id)
                    except:
                        error = 'Hospital in request could not be found! Please try again.'
                        args['error'] = error
                        return render(request,'w_details_hospital.html',args)
                    departments = Department.objects.filter(department_id__in =
                                                            DoctorRegistration.objects.filter(
                                                                doctor_org = org_id,
                                                                doctor_hospital = hospital_id).values_list('doctor_department', flat=True))
                    # print(departments)
                    # doctors = list(DoctorRegistration.objects.filter(doctor_org = org_id, doctor_hospital = hospital_id))
                    args['depts'] = departments
                    args['hospital'] = hospital
                    if hospital.hospital_settings is None:
                        args['isSettings'] = False
                    else:
                        settings = hospital.hospital_settings
                        args['isSettings'] = True
                        args['email']         = settings.settings_email
                        args['email_smtp']    = settings.settings_email_smtp
                        args['voice_rate']    = settings.settings_voice_rate
                        args['video_rate']    = settings.settings_video_rate
                        args['status']        = settings.settings_status
                        args['isVoice'] = False
                        args['isVideo'] = False
                        if organisation.org_settings.orgsettings_subscription == 'C':
                            args['isVoice'] = True
                        else:
                            args['isVoice'] = True
                            args['isVideo'] = True
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
                                settings = HospitalSettings()
                                settings.settings_status = True
                                settings.save()
                                hospital.hospital_settings = settings
                                hospital.save()
                            args['new_hospital_added'] = hospital.hospital_name
                            args['new_hospital_id'] = hospital.hospital_id
                            return render(request,'w_dashboard_hospital.html',args)
                        except:
                            traceback.print_exc()
                            error = 'Error saving new hospital!'
                else:

                    print(formHospital.errors)
                    print(formAddress.errors)
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

""" Doctor views for webportal """

def doctor_dashboard(request):
    if isUserLogged(request):
        return render(request,'w_dashboard_doctor.html')
    else:
        return userSessionExpired()


def doctor_new(request, org_id=0):
    error = None
    args = {}
    if isUserLogged(request):
        if isUserRequestValid(request,org_id):
            if request.POST:
                formAddress = AddressForm(request.POST)
                formDocDetails = PortalDoctorDetailsForm(request.POST)
                formDocRegistration = PortalDoctorRegistrationForm(org_id,request.POST)
                print "POST Request"
                if (formDocRegistration.is_valid() & formDocDetails.is_valid() & formAddress.is_valid()):
                    print "Form Valid"
                    email = formDocRegistration.cleaned_data['doctor_email']
                    hospitalID = formDocRegistration.cleaned_data['hospital_choice']
                    deptID = formDocRegistration.cleaned_data['dept_choice']
                    registeredDoc = DoctorRegistration.objects.filter(doctor_org = org_id, doctor_email__iexact = email)
                    if len(registeredDoc)==0 :

                        try:
                            randomPassword = None
                            organisation = Organisation.objects.get(org_id = org_id)
                            hospital = Hospital.objects.get(hospital_org = org_id, hospital_id = hospitalID)
                            department = Department.objects.get(department_org = org_id, department_id = deptID)
                            with transaction.atomic():
                                docReg = formDocRegistration.save(commit=False)
                                docDet = formDocDetails.save(commit=False)
                                docAddress = formAddress.save()

                                docReg.doctor_org = organisation
                                docReg.doctor_department = department
                                docReg.doctor_hospital = hospital
                                docReg.doctor_status = True
                                randomPassword = generateRandomPassword()
                                docReg.doctor_password = getPasswordHash(randomPassword)
                                docReg.save()
                                docReg.doctor_code = generateDoctorCode(org_id,hospital.hospital_branch_code,docReg.doctor_id)
                                docReg.save()

                                docDet.doctor_address = docAddress
                                docDet.doctor_id = docReg
                                docDet.save()

                            send_mail_to_doctor(docReg,randomPassword,organisation.org_identifier)

                            args['new_doctor_added'] = docDet.doctor_first_name+' '+docDet.doctor_last_name
                            args['new_doctor_id'] = docReg.doctor_id
                            return render(request,'w_dashboard_doctor.html',args)
                        except:
                            traceback.print_exc()
                            error = "Error while adding doctor"
                    else:
                        print registeredDoc
                        error = "Doctor Email Id is already registered! Please try a unique email id."
                else:
                    traceback.print_exc()
                    error = "Invalid form!"
            else:
                formAddress = AddressForm()
                formDocDetails = PortalDoctorDetailsForm()
                formDocRegistration = PortalDoctorRegistrationForm(org_id)
        else:
            error = "Invalid Request!"
            formAddress = AddressForm()
            formDocDetails = PortalDoctorDetailsForm()
            formDocRegistration = PortalDoctorRegistrationForm(org_id)
        args.update(csrf(request))
        args['error'] = error
        args['formAddress'] = formAddress
        args['formDocDetails'] = formDocDetails
        args['formDocRegistration'] = formDocRegistration
        return render(request,'w_new_doctor.html',args)
    else:
        return userSessionExpired()


def doctor_details(request,org_id=0,doctor_id=0):
    error = None
    args = {}
    organisation = None
    docReg = None
    docDetails = None
    if isUserLogged(request):
        if 'setting' in request.GET :
            result = request.GET['setting']
            args['result'] = result
        if isUserRequestValid(request,org_id):
            if org_id!=0:
                organisation = Organisation.objects.get(org_id__exact = org_id)
                args['org'] = organisation
                if doctor_id !=0 :
                    try:
                        docReg = DoctorRegistration.objects.get(doctor_org = org_id, doctor_id = doctor_id)
                        docDetails = DoctorDetails.objects.get(doctor_id = doctor_id)
                    except:
                        error = 'Doctor in request could not be found! Please try again.'
                        args['error'] = error
                        return render(request,'w_details_doctor.html',args)
                    doctor = {}
                    doctor['docReg'] = docReg
                    doctor['docDetails'] = docDetails
                    args['doctor'] = doctor
                    if docReg.doctor_settings is None:
                        args['isSettings'] = False
                    else:
                        settings = docReg.doctor_settings
                        args['isSettings'] = True
                        args['isVoice']       = settings.settings_voice
                        args['isVideo']       = settings.settings_video
                        args['isPrescription'] = settings.settings_eprescription
                        args['voice_rate']    = settings.settings_voice_rate
                        args['video_rate']    = settings.settings_video_rate
                        args['status']        = settings.settings_status

                        args['isVoiceEnabled'] = False
                        args['isVideoEnabled'] = False
                        args['isPrescriptionEnabled'] = False
                        if organisation.org_settings.orgsettings_subscription == 'C':
                            args['isVoiceEnabled'] = True
                        elif organisation.org_settings.orgsettings_subscription == 'CV':
                            args['isVoiceEnabled'] = True
                            args['isVideoEnabled'] = True
                        elif organisation.org_settings.orgsettings_subscription == 'CVP':
                            args['isVoiceEnabled'] = True
                            args['isVideoEnabled'] = True
                            args['isPrescriptionEnabled'] = True
            else:
                error = 'Invalid request'
            formDoctorChoice = PortalDoctorSelectionForm(org_id)
            args['formDoctorChoice'] = formDoctorChoice
            return render(request,'w_details_doctor.html',args)
        else:
            error = 'Invalid Request'
        args['error'] = error
        return render(request,'w_details_doctor.html',args)
    else:
        return userSessionExpired()

""" End of doctor views """


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
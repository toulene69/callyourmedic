from django.shortcuts import render , render_to_response
from django.http import HttpResponse , HttpResponseRedirect , Http404
from django.template.loader import get_template
from django.core.context_processors import csrf
from django.db import IntegrityError, transaction
import traceback
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#model imports
from models import User
from addresses.models import Address
from organisations.models import Organisation, Apikey
from hospitals.models import Department, Hospital
from doctors.models import DoctorRegistration, DoctorDetails
from webportal.models import createSuperUserAndGroup

#form imports
from addresses.forms import AddressForm
from forms import CYMUserLoginForm , CYMOrganisationCreationForm , CYMOrganisationSelectionForm, CYMOrgHospitalSelectionForm

from utils.session_utils import isUserLogged , createUserSession , destroyUserSession , userSessionExpired
from utils.app_utils import generateAPIKey

import logging

logger = logging.getLogger('cym')

"""Login/Logout"""
def login(request):
	args = {}
	if isUserLogged(request):
		return HttpResponseRedirect('/cym/dashboard')
	else:
		error = None
		if request.POST:
			formLogin = CYMUserLoginForm(request.POST)
			if formLogin.is_valid():
				username = formLogin.cleaned_data['user_name']
				password = formLogin.cleaned_data['password']
				obj = None
				try:
					obj = User.objects.get(usr_email__iexact = username)
				except (KeyError, User.DoesNotExist):
					error = "Username or password incorrect"
					logger.exception("User does not exists "+username)
					args.update(csrf(request))
					args['formLogin'] = formLogin
					args['error'] = error
					return render_to_response('login.html',args)
				if obj.usr_password == password:
					try:
						createUserSession(request,obj)
						return HttpResponseRedirect('/cym/dashboard')
					except:
						error = "Session error occurred"
						logger.exception("Session creation error occured for user "+username)
						args.update(csrf(request))
						args['formLogin'] = formLogin
						args['error'] = error
						return render_to_response('login.html',args)
				else:
					logger.info("Incorrect password for user "+username)
					error = "Username or password incorrect"
			else:
				print ("*********Form invalid")
		else:
			formLogin = CYMUserLoginForm()
			request.session.set_test_cookie()
		if 'sessionError' in request.GET:
			if request.GET['sessionError'] == '100':
				args['sessionError'] = True
		args.update(csrf(request))
		args['formLogin'] = formLogin
		args['error'] = error
		return render_to_response('login.html',args)

def logout(request):
	temp = get_template('logout.html')
	destroyUserSession(request)
	html = temp.render()
	return HttpResponse(html)

"""Login/Logout Ends"""

def dashboard(request):
	if isUserLogged(request):
		usr_details = request.session['usr_details']
		return render_to_response('dashboard.html',usr_details)
	else:
		return userSessionExpired()


""" Organisation Views """
def org_dashboard(request):
	if isUserLogged(request):
		usr_details = request.session['usr_details']
		return render_to_response('org_dashboard.html',usr_details)
	else:
		return userSessionExpired()

def org_details(request,org_id=0):
	if isUserLogged(request):
		args = {}
		usr_details = request.session['usr_details']
		organisation = None
		department = None
		if org_id != 0:
			orgID = org_id
			try:
				organisation = Organisation.objects.get(org_id = orgID)
				department = Department.objects.filter(department_org = orgID)
			except:
				logger.exception("Organisation ID "+str(orgID)+" not found")
			args['org'] = organisation
			args['depts'] = department
		formOrgChoice = CYMOrganisationSelectionForm()
		args['usr_details'] = usr_details
		args['formOrgChoice'] = formOrgChoice
		return render_to_response('org_details.html',args)
	else:
		return userSessionExpired()

def org_new(request):
	error = None
	args = {}
	if isUserLogged(request):
		usr_details = request.session['usr_details']
		if request.POST:
			formOrg = CYMOrganisationCreationForm(request.POST)
			formAddress = AddressForm(request.POST)
			if formOrg.is_valid() & formAddress.is_valid():

				address = Address()
				organisation = Organisation()
				address.address_line1 = formAddress.cleaned_data['address_line1']
				address.address_line2 = formAddress.cleaned_data['address_line2']
				address.address_city = formAddress.cleaned_data['address_city']
				address.address_state = formAddress.cleaned_data['address_state']
				pin = formAddress.cleaned_data['address_pincode']
				address.address_pincode = pin
				address.address_status = True

				organisation.org_name = formOrg.cleaned_data['org_name']
				organisation.org_brand = formOrg.cleaned_data['org_brand']
				organisation.org_phone = formOrg.cleaned_data['org_phone']
				organisation.org_active = formOrg.cleaned_data['org_active']
				organisation.org_emailid = formOrg.cleaned_data['org_emailid']
				try:
					with transaction.atomic():
						address.save()
						organisation.org_address = address
						organisation.save()
						organisation.org_billing_id = organisation.org_id
						identifier = str(organisation.org_id) + '_' + organisation.org_brand
						organisation.org_identifier = identifier.replace(" ", "")
						organisation.save()
						success = createSuperUserAndGroup(organisation.org_emailid,organisation.org_phone,organisation,'Super Admin')
						if success:
							print 'Super User Created'
						else:
							print 'Error while creating super user'
					args['usr_details'] = usr_details
					args['new_org_added'] = organisation.org_name
					args['new_org_id'] = organisation.org_id
					return render_to_response('org_dashboard.html',args)
				except IntegrityError:
					error = 'Error creating new organisation'
			else:
				error = 'Error creating new organisation'
		else:
			formOrg = CYMOrganisationCreationForm()
			formAddress = AddressForm()
		args.update(csrf(request))
		args['formOrg'] = formOrg
		args['formAddress'] = formAddress
		args['usr_details'] = usr_details
		args['error'] = error
		return render_to_response('org_new.html',args)
	else:
		return userSessionExpired()

def org_requests(request,org_id=0):
	temp = get_template('org_requests.html')
	html = temp.render()
	return HttpResponse(html)

def org_create_apikey(request,org_id=0):
	error = None
	args = {}
	if isUserLogged(request):
		usr_details = request.session['usr_details']
		try:
			organisation = Organisation.objects.get(org_id = org_id)
			key = generateAPIKey()
			apikey = Apikey(apikey_org = organisation,apikey_key = key)
			try:
				apikey.save()
			except:
				traceback.print_exc()
				error = "Key Generation Failed! Try Again."
		except(KeyError, Organisation.DoesNotExist):
			error = "Username or password incorrect"
		args['error'] = error
		args['usr_details'] = usr_details
		return HttpResponseRedirect('/cym/organisationdetails/'+str(org_id)+'/')
	else:
		return userSessionExpired()

def search(request,org_id=0,hospital_id=0):
	if isUserLogged(request):
		args = {}
		usr_details = request.session['usr_details']
		args['usr_details'] = usr_details
		return render_to_response('org_search.html',args)
	else:
		return userSessionExpired()


""" Organisation Views Ends"""


""" User Views """

# def usr_dashboard(request):
# 	if isUserLogged(request):
# 		usr_details = request.session['usr_details']
# 		users = User.objects.all()
# 		paginator = Paginator(users, 25) # Show 25 contacts per page
# 		page = request.GET.get('page')
# 		try:
# 			users = paginator.page(page)
# 		except PageNotAnInteger:
#         	# If page is not an integer, deliver first page.
# 			users = paginator.page(1)
# 		except EmptyPage:
#         	# If page is out of range (e.g. 9999), deliver last page of results.
# 			users = paginator.page(paginator.num_pages)
# 		return render_to_response('usr_dashboard.html', {"users": users,"usr_details":usr_details})
# 		#return render_to_response('usr_dashboard.html',usr_details)
# 	else:
# 		return HttpResponseRedirect('/cymlogin')

def usr_dashboard(request):
	if isUserLogged(request):
		usr_details = request.session['usr_details']
		return render_to_response('usr_dashboard.html', usr_details)
	else:
		return userSessionExpired()

def usr_users(request):
	if isUserLogged(request):
		usr_details = request.session['usr_details']
		return render_to_response('usr_user.html', usr_details)
	else:
		return userSessionExpired()

def usr_group(request):
	if isUserLogged(request):
		usr_details = request.session['usr_details']
		return render_to_response('usr_group.html', usr_details)
	else:
		return userSessionExpired()

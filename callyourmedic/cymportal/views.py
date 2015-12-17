from django.shortcuts import render , render_to_response
from django.http import HttpResponse , HttpResponseRedirect , Http404
from django.template.loader import get_template
from django.core.context_processors import csrf
from django.db import IntegrityError, transaction

import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#model imports
from models import User
from addresses.models import Address
from organisations.models import Organisation
from hospitals.models import Department
from webportal.models import createSuperUserAndGroup

#form imports
from addresses.forms import AddressForm
from forms import CYMUserLoginForm , CYMOrganisationCreationForm , CYMOrganisationSelectionForm

from utils.session_utils import isUserLogged , createUserSession , destroyUserSession , userSessionExpired

import logging

logger = logging.getLogger(__name__)

"""Login/Logout"""
def login(request):
	if isUserLogged(request):
		return HttpResponseRedirect('/cym/dashboard')
	else:
		error = None
		if request.POST:
			formLogin = CYMUserLoginForm(request.POST)
			if formLogin.is_valid():
				username = formLogin.cleaned_data['user_name']
				password = formLogin.cleaned_data['password']
				try:
					obj = User.objects.get(usr_email__iexact = username)
					print (obj.usr_password)
					if obj.usr_password == password:
						createUserSession(request,obj)
						return HttpResponseRedirect('/cym/dashboard')
					else:
						print ("********* Password incorrect")
						error = "Username or password incorrect"
				except (KeyError, User.DoesNotExist):
					error = "Username or password incorrect"
					print ("********* User does not exists")
			else:
				print ("*********Form invalid")
		else:
			formLogin = CYMUserLoginForm()
			request.session.set_test_cookie()
		args = {}
		if 'sessionError' in request.GET:
			if request.GET['sessionError'] == '100':
				print ('******* Session Expired ***')
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
		if org_id != 0:
			orgID = org_id
			organisation = Organisation.objects.get(org_id = orgID)
			department = Department.objects.filter(department_org = orgID)
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

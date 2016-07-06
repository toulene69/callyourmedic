__author__ = 'apoorv'

from django.http import HttpRequest , HttpResponse , JsonResponse , HttpResponseRedirect , Http404
from django.shortcuts import render_to_response, render
from django.core.context_processors import csrf
import traceback
from django.utils import timezone
import pytz, time
from django.db import IntegrityError, transaction

from organisations.models import Organisation, OrgSettings
from models import WebUser, WebGroup, send_mail_for_group, send_mail_for_user
from hospitals.models import Hospital, Department, HospitalSettings
from doctors.models import DoctorRegistration, DoctorDetails, DoctorSettings
# utils imports
from utils.web_portal_session_utils import isUserLogged , userSessionExpired, isUserRequestValid
from utils.app_utils import get_permission , get_active_status, generateRandomPassword, get_subscription_type, getPasswordHash

# form imports
from forms import PortalUserCreationForm, PortalUserGroupCreationForm, PortalDepartmentCreationForm, PortalOrgSettingsForm, PortalHospitalSettingsForm, PortalDoctorSettingsForm

from mailer.views import *

import logging

logger = logging.getLogger('webportal')

timezone.activate(pytz.timezone("Asia/Kolkata"))
current_tz = timezone.get_current_timezone()
""" For webportal org"""

def org_getdepartments(request,org_id=0):
	res = {
    	"recordsTotal": 0,
		"data" : []
		}
	if request.is_ajax() | True:
		try:
			departments = list(Department.objects.filter(department_org__exact = org_id))
			for department in departments:
				dept = {}
				dept['name'] = (department.department_name)
				dept['description'] = (department.department_description)
				dept['code'] = (department.department_code)
				dept['status'] = department.department_status
				dept['date_add'] = department.department_date_added
				dept['org_id'] = org_id
				dept['dept_id'] = department.department_id
				res['data'].append(dept)
		except:
			print "error retrieving users"
		res['recordsTotal'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Users fetch request not proper")

def org_departmentnew(request,org_id=0):
	error = None
	formError = False
	args = {}
	if isUserLogged(request):
		if request.POST:
			deptCreationForm = PortalDepartmentCreationForm(request.POST)
			if deptCreationForm.is_valid():
				deptcode = deptCreationForm.cleaned_data['department_code']
				departments = list(Department.objects.filter(department_org__exact = org_id, department_code__iexact = deptcode))
				if len(departments) == 0:
					try:
						dept = deptCreationForm.save(commit=False)
						org = Organisation.objects.get(org_id__exact = org_id)
						dept.department_org = org
						dept.department_status = True
						dept.save()
						return render(request,'w_department_org.html')
					except:
						traceback.print_exc()
						error = "Error creating department"
						formError = True
						args['error'] = error
						args['formError'] = formError
						return render(request,'w_department_org.html',args)
				else:
					error = 'Department Code already present. Insert a unique code'
					formError = True
					args['error'] = error
					args['formError'] = formError
					return render(request,'w_department_org.html',args)
			else:
				error = "Invalid form submitted"
				formError = True
				args['error'] = error
				args['formError'] = formError
				return render(request,'w_department_org.html',args)
		else:
			deptCreationForm = PortalDepartmentCreationForm()
		args.update(csrf(request))
		args['error'] = error
		args['deptCreationForm'] = deptCreationForm
		return render(request,'w_newdepartment_org.html',args)
	else:
		html = '<div class="modal-body" id="modal-body-createGroup">User Session Expired! <a href="/portal/?sessionError=100">Login</a></div>'
		return HttpResponse(html)

def org_departmentedit(request,org_id=0,dept_id=0):
	error = None
	formError = False
	args = {}
	if isUserLogged(request) is False:
		html = '<div class="modal-body" id="modal-body-createGroup">User Session Expired! <a href="/portal/?sessionError=100">Login</a></div>'
		return HttpResponse(html)

	if org_id == 0 or dept_id == 0:
		html = '<div class="modal-body" id="modal-body-createGroup">Request informations not correct. Please try again!</div>'
		return HttpResponse(html)

	if isUserRequestValid(request,org_id) is False:
		html = '<div class="modal-body" id="modal-body-createGroup">Permission Denied.</div>'
		return HttpResponse(html)
	deptEditForm = None
	department = None
	try:
		department = Department.objects.get(department_id = dept_id, department_org = org_id)
	except:
		logger.error("Error fetching department for editing with dept_id "+str(dept_id)+" for org_id "+str(org_id))
		traceback.print_exc()
		html = '<div class="modal-body" id="modal-body-createGroup">Department details could not be retrived to edit. Try again!</div>'
		return HttpResponse(html)

	if request.is_ajax():
		deptEditForm = PortalDepartmentCreationForm(instance = department)
		args['dept'] = department.department_id
	elif request.POST:
		deptEditForm = PortalDepartmentCreationForm(request.POST)
		if deptEditForm.is_valid():
			department.department_name = deptEditForm.cleaned_data['department_name']
			department.department_code = deptEditForm.cleaned_data['department_code']
			department.department_description = deptEditForm.cleaned_data['department_description']
			department.department_status = deptEditForm.cleaned_data['department_status']
			try:
				department.save()
			except:
				logger.error("Error while saving department after editing with dept_id "+str(dept_id)+" for org_id "+str(org_id))
				traceback.print_exc()
				error = "Error while saving the details. Please try again."
				formError = True
				args['error'] = error
				args['formError'] = formError
				return render(request,'w_department_org.html',args)

			return render(request,'w_department_org.html')
		else:
			error = "Invalid form submitted"
			formError = True
			args['error'] = error
			args['formError'] = formError
			return render(request,'w_department_org.html',args)
	else:
		html = '<div class="modal-body" id="modal-body-createGroup">Improper request type</div>'
		return HttpResponse(html)

	args.update(csrf(request))
	args['error'] = error
	args['deptCreationForm'] = deptEditForm
	args['isEdit'] = True
	return render(request,'w_newdepartment_org.html',args)



""" Ends webportal org"""


""" FOR WebPortal Users"""
def usr_getusers(request,org_id=0):
	res = {
    	"recordsTotal": 0,
		"data" : []
		}
	if request.is_ajax() | True:
		try:
			users = list(WebUser.objects.filter(usr_org__exact = org_id))
			for user in users:
				usr = {}
				usr['name'] = (user.usr_first_name)
				usr['username'] = (user.usr_email)
				usr['phonenumber'] = (user.usr_phone)
				usr['usergroup'] = (user.usr_group.grp_name)
				usr['status'] = (user.usr_status)
				res['data'].append(usr)
		except:
			print "error retrieving users"

		res['recordsTotal'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Users fetch request not proper")

def usr_getgroups(request,org_id=0):
	res = {
    	"recordsTotal": 0,
		"data" : []
		}
	if request.is_ajax() | True:
		x = []
		groups = list(WebGroup.objects.filter(grp_org_id__exact = org_id).order_by('grp_id'))
		i=0
		for group in groups:
			grp = {}
			grp['name'] = (group.grp_name)
			grp['org'] = (get_permission(group.grp_org))
			grp['hospital'] = (get_permission(group.grp_hospital))
			grp['doctor'] = (get_permission(group.grp_doctor))
			grp['patient'] = (get_permission(group.grp_patients))
			grp['call'] = (get_permission(group.grp_call))
			grp['transaction'] = (get_permission(group.grp_transaction))
			grp['user'] = (get_permission(group.grp_user))
			grp['groupid'] = group.grp_id
			grp['status'] = group.grp_status
			res['data'].append(grp)
		res['recordsTotal'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Groups fetch request not proper")

def usr_usrgroupnew(request,org_id):
	error = None
	formError = False
	args = {}
	if isUserLogged(request):
		if request.POST:
			groupCreationForm = PortalUserGroupCreationForm(request.POST)
			if groupCreationForm.is_valid():
				grpName = groupCreationForm.cleaned_data['grp_name']
				groups = list(WebGroup.objects.filter(grp_org_id__exact = org_id, grp_name__iexact = grpName))
				if len(groups) == 0:
					try:
						groupForm = groupCreationForm.save(commit=False)
						org = Organisation.objects.get(org_id__exact = org_id)
						groupForm.grp_org_id = org
						groupForm.grp_status = True
						groupForm.save()
						if groupForm.isSuperGroup():
							groupForm.is_super = True
							groupForm.save()

						users = list(WebUser.objects.filter(usr_group__in = WebGroup.objects.filter(is_super = True, grp_org_id__exact = org)).values('usr_email'))
						usr = []
						if users is not None and len(users) != 0:
							for user in users:
								usr.append(user['usr_email'])
						send_mail_for_group(usr, groupForm)
						return render(request,'w_group_usr.html')
					except:
						print '********* form invalid'
						traceback.print_exc()
						error = 'Error creating group. Please try again'
						formError = True
						args['formError'] = formError
						args['error'] = error
						return render(request,'w_group_usr.html', args)
				else:
					error = "Group name : "+grpName+" already exists. Please insert a unique name!"
					formError = True
					args['formError'] = formError
					args['error'] = error
					return render(request,'w_group_usr.html', args)
			else:
				print '********form incomplete'
				error = 'Group creation form incomplete. Please try again!'
				formError = True
				args['formError'] = formError
				args['error'] = error
				return render(request,'w_group_usr.html', args)
		else:
			groupCreationForm = PortalUserGroupCreationForm()

		args.update(csrf(request))
		args['groupCreationForm'] = groupCreationForm
		return render(request,'w_newgroup_usr.html',args)
	else:
		html = '<div class="modal-body" id="modal-body-createGroup">User Session Expired! <a href="/portal/?sessionError=100">Login</a></div>'
		return HttpResponse(html)


def usr_usernew(request,org_id=0):
	error = None
	formError = False
	args = {}
	if isUserLogged(request):
		if request.POST:
			userCreationForm = PortalUserCreationForm(org_id,request.POST)
			if userCreationForm.is_valid():
				emailid = userCreationForm.cleaned_data['usr_email']
				print emailid
				user = list(WebUser.objects.filter(usr_org__exact = org_id, usr_email__iexact = emailid))
				if len(user) == 0:
					try:
						userForm = userCreationForm.save(commit=False)
						org = Organisation.objects.get(org_id__exact = org_id)
						userForm.usr_org = org
						randomPassword = generateRandomPassword()
						userForm.usr_password = getPasswordHash(randomPassword)
						userForm.usr_status = True
						userForm.save()
						send_mail_for_user(userForm,randomPassword,org.org_identifier)
						return render(request,'w_users_usr.html')
					except:
						print '********* form invalid'
						traceback.print_exc()
						error = 'Error creating user. Please try again'
						formError = True
						args['formError'] = formError
						args['error'] = error
						return render(request,'w_users_usr.html', args)
				else:
					formError = True
					error = "User email id already exists. Please insert a unique email id!"
					args['formError'] = formError
					args['error'] = error
					return render(request,'w_users_usr.html', args)
			else:
				print '********* form incomplete'
				print userCreationForm.errors
				error = 'User creation form incomplete. Please try again!'
				formError = True
				args['formError'] = formError
				args['error'] = error
				return render(request,'w_users_usr.html', args)
		else:
			userCreationForm = PortalUserCreationForm(org_id)
		args.update(csrf(request))
		args['userCreationForm'] = userCreationForm
		return render(request,'w_newuser_usr.html',args)
	else:
		html = '<div class="modal-body" id="modal-body-createGroup">User Session Expired! <a href="/portal/?sessionError=100">Login</a></div>'
		return HttpResponse(html)

def usr_groupedit(request,org_id=0,grp_id=0):
	error = None
	formError = False
	args = {}
	if isUserLogged(request) is False:
		html = '<div class="modal-body" id="modal-body-createGroup">User Session Expired! <a href="/portal/?sessionError=100">Login</a></div>'
		return HttpResponse(html)

	if org_id == 0 or grp_id == 0:
		html = '<div class="modal-body" id="modal-body-createGroup">Request informations not correct. Please try again!</div>'
		return HttpResponse(html)

	if isUserRequestValid(request,org_id) is False:
		html = '<div class="modal-body" id="modal-body-createGroup">Permission Denied.</div>'
		return HttpResponse(html)

	groupEditForm = None
	group = None
	try:
		group = WebGroup.objects.get(grp_id = grp_id, grp_org_id = org_id)
	except:
		logger.error("Error fetching group for editing with grp_id "+str(grp_id)+" for org_id "+str(org_id))
		traceback.print_exc()
		html = '<div class="modal-body" id="modal-body-createGroup">Department details could not be retrived to edit. Try again!</div>'
		return HttpResponse(html)

	if request.is_ajax():
		groupEditForm = PortalUserGroupCreationForm(instance = group)
		args['grp_id'] = group.grp_id
	elif request.POST:
		groupEditForm = PortalUserGroupCreationForm(request.POST)
		if groupEditForm.is_valid():
			group.grp_name = groupEditForm.cleaned_data['grp_name']
			group.grp_org = groupEditForm.cleaned_data['grp_org']
			group.grp_hospital = groupEditForm.cleaned_data['grp_hospital']
			group.grp_doctor = groupEditForm.cleaned_data['grp_doctor']
			group.grp_patients = groupEditForm.cleaned_data['grp_patients']
			group.grp_transaction = groupEditForm.cleaned_data['grp_transaction']
			group.grp_call = groupEditForm.cleaned_data['grp_call']
			group.grp_user = groupEditForm.cleaned_data['grp_user']
			group.grp_status = groupEditForm.cleaned_data['grp_status']
			try:
				group.save()

			except:
				logger.error("Error while saving group after editing with grp_id "+str(grp_id)+" for org_id "+str(org_id))
				traceback.print_exc()
				error = 'Error while saving the details. Please try again.'
				formError = True
				args['formError'] = formError
				args['error'] = error
				return render(request,'w_group_usr.html', args)

			return render(request,'w_group_usr.html')
		else:
			error = "Invalid form submitted. Please fill the details correctly."
			formError = True
			args['error'] = error
			args['formError'] = formError
			return render(request,'w_group_usr.html', args)
	else:
		html = '<div class="modal-body" id="modal-body-createGroup">Improper request type</div>'
		return HttpResponse(html)

	args.update(csrf(request))
	args['error'] = error
	args['groupCreationForm'] = groupEditForm
	args['isEdit'] = True
	return render(request,'w_newgroup_usr.html',args)

""" ENDS WebPortal Users """

""" WebPortal Hospital """
def hospital_check_branch_code(request,org_id=0):
	result = {'present':True, 'error':None}
	if request.is_ajax() | True:
		if 'branchcode' in request.GET:
			inputVal = request.GET['branchcode']
			print inputVal
			try:
				hospitalPresent = list(Hospital.objects.filter(hospital_branch_code__iexact = inputVal, hospital_org__exact = org_id))
			except:
				print "DB Error"
			if len(hospitalPresent) == 0:
				result['present'] = False
	else:
		result['present'] = False
		result['error'] = 'Ajax Error'
	return JsonResponse(result, safe=False)

def hospital_gethospitals(request,org_id=0):
	res = {
    	"recordsTotal": 0,
		"data" : []
		}
	if request.is_ajax() | True:
		x = []
		hospitals = list(Hospital.objects.filter(hospital_org__exact = org_id).order_by('hospital_id'))
		i=0
		for hospital in hospitals:
			hspt = {}
			hspt['name'] = (hospital.hospital_name)
			hspt['code'] = (hospital.hospital_branch_code)
			hspt['city'] = (hospital.hospital_address.address_city)
			hspt['state'] = (hospital.hospital_address.address_state)
			hspt['phone'] = (hospital.hospital_phone1)
			hspt['joined'] = (hospital.hospital_date_joined)
			hspt['hospital_id'] = hospital.hospital_id
			hspt['org_id'] = org_id
			hspt['status'] = hospital.hospital_status
			# hspt.append('<a href="/web/'+str(org_id)+'/hospitaldetails/'+str(hospital.hospital_id)+'/">View</a>')
			res['data'].append(hspt)
		res['recordsTotal'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Groups fetch request not proper")

""" Ends WebPortal Hospital"""


""" Webportal Doctors"""
def doctor_getdoctors(request, org_id=0):
	res = {
    	"recordsTotal": 0,
		"data" : []
		}
	if request.is_ajax() | True:
		x = []
		try:
			doctors = list(DoctorRegistration.objects.filter(doctor_org__exact = org_id).order_by('doctor_id'))
			i=0
			for doctor in doctors:
				doc = {}
				details = DoctorDetails.objects.get(doctor_id__exact = doctor.doctor_id)
				doc['name'] = (details.doctor_first_name+' '+details.doctor_last_name)
				doc['department'] = (doctor.doctor_department.department_name)
				doc['code'] = (doctor.doctor_code)
				doc['qualification'] = (details.doctor_qualification)
				doc['experience'] = (details.doctor_experience)
				doc['email'] = (doctor.doctor_email)
				doc['phone'] = (str(details.doctor_phone1)+', '+str(details.doctor_phone2))
				doc['joined'] = details.doctor_date_joined
				doc['org_id'] = org_id
				doc['doctor_id'] = doctor.doctor_id
				doc['status'] = doctor.doctor_status
				# doc.append('<a href="/web/'+ str(org_id) +'/doctordetails/'+ str(doctor.doctor_id) +'">View</a>')
				res['data'].append(doc)
		except:
			traceback.print_exc()
		res['recordsTotal'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Groups fetch request not proper")

def doctor_getdoctorsforhospitals(request,org_id=0,hospital_id=0):
	res = {
		"draw": 1,
    	"recordsTotal": 0,
    	"recordsFiltered": 0,
		"data" : []
		}
	if request.is_ajax() | True:
		x = []
		try:
			doctors = list(DoctorRegistration.objects.filter(doctor_org__exact = org_id,doctor_hospital = hospital_id).order_by('doctor_id'))
			i=0
			for doctor in doctors:
				doc = {}
				details = DoctorDetails.objects.get(doctor_id__exact = doctor.doctor_id)
				doc['name'] = (details.doctor_first_name+' '+details.doctor_last_name)
				doc['department'] = (doctor.doctor_department.department_name)
				doc['code'] = (doctor.doctor_code)
				doc['qualification'] = (details.doctor_qualification)
				doc['experience'] = (details.doctor_experience)
				doc['email'] = (doctor.doctor_email)
				doc['phone'] = (str(details.doctor_phone1)+', '+str(details.doctor_phone2))
				doc['joined'] = details.doctor_date_joined
				doc['org_id'] = org_id
				doc['doctor_id'] = doctor.doctor_id
				doc['status'] = doctor.doctor_status
				# doc.append('<a href="/web/'+ str(org_id) +'/doctordetails/'+ str(doctor.doctor_id) +'">View</a>')
				res['data'].append(doc)
		except:
			traceback.print_exc()
		res['recordsTotal'] = len(res['data'])
		res['recordsFiltered'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Groups fetch request not proper")


""" Ends Webportal doctors"""

""" Settings """
def settings_edit(request,org_id=0,hospital_id=0,doctor_id=0):
	args = {}
	organisation = None
	hospital = None
	doctor = None
	isSettings = False
	isOrg = False
	isHospital = False
	isDoctor = False
	if org_id != 0 and hospital_id == 0 and doctor_id == 0:
		isOrg = True
	elif org_id != 0 and hospital_id != 0 and doctor_id == 0:
		isHospital = True
	elif org_id != 0 and hospital_id != 0 and doctor_id != 0:
		isDoctor = True
	else:
		html = '<div class="modal-body" id="modal-body-createGroup">Improper Request. Please try again!</div>'
		return HttpResponse(html)

	if isOrg:
		orgSettingsForm = None
		try:
			organisation = Organisation.objects.get(org_id = org_id)
		except:
			html = '<div class="modal-body" id="modal-body-createGroup">Organisation could not be found. Please try again!</div>'
			return HttpResponse(html)
		if organisation.org_id != request.session['org_id']:
			html = '<div class="modal-body" id="modal-body-createGroup">User Not authorized for settings changes for organisation in request!</div>'
			return HttpResponse(html)

		if request.POST:
			orgSettingsForm = PortalOrgSettingsForm(request.POST)
			settings = None
			if orgSettingsForm.is_valid():
				if organisation.org_settings is None:
					settings = OrgSettings()
				else:
					settings = organisation.org_settings
				settings.orgsettings_billing_cycle = orgSettingsForm.cleaned_data['orgsettings_billing_cycle']
				settings.orgsettings_email = orgSettingsForm.cleaned_data['orgsettings_email']
				settings.orgsettings_email_smtp = orgSettingsForm.cleaned_data['orgsettings_email_smtp']
				settings.orgsettings_voice_rate = orgSettingsForm.cleaned_data['orgsettings_voice_rate']
				settings.orgsettings_video_rate = orgSettingsForm.cleaned_data['orgsettings_video_rate']
				try:
					with transaction.atomic():
						settings.save()
						if organisation.org_settings is None:
							organisation.org_settings = settings
						organisation.save()
					return HttpResponseRedirect('/web/org/?setting=updated')
				except:
					traceback.print_exc()
					print '********* form invalid'
					error = 'Error updating settings. Please try again'
					formError = True
					args['formError'] = formError
					args['error'] = error
					return HttpResponseRedirect('/web/org/?setting=error')

			else:
				print '********form incomplete'
				error = 'Settings form invalid. Please try again!'
				formError = True
				args['formError'] = formError
				args['error'] = error
				args['errorReason'] = orgSettingsForm.errors
				return HttpResponseRedirect('/web/org/?setting=incomplete')
		else:
			args['isVoice'] = False
			args['isVideo'] = False
			if organisation.org_settings is None:
				orgSettingsForm = PortalOrgSettingsForm()
			else:
				orgSettingsForm = PortalOrgSettingsForm(instance = organisation.org_settings)
				if organisation.org_settings.orgsettings_subscription == 'C':
					args['isVoice'] = True
				else:
					args['isVoice'] = True
					args['isVideo'] = True
			args['orgSettingsForm'] = orgSettingsForm
			return render(request,'w_settings_org.html',args)

	elif isHospital:
		hospitalSettingsForm = None
		try:
			organisation = Organisation.objects.get(org_id = org_id)
		except:
			html = '<div class="modal-body" id="modal-body-createGroup">Organisation could not be found. Please try again!</div>'
			return HttpResponse(html)
		if organisation.org_id != request.session['org_id']:
			html = '<div class="modal-body" id="modal-body-createGroup">User Not authorized for settings changes for organisation in request!</div>'
			return HttpResponse(html)
		try:
			hospital = Hospital.objects.get( hospital_id = hospital_id,hospital_org = org_id)
		except:
			html = '<div class="modal-body" id="modal-body-createGroup">Hospital could not be found to edit settings!</div>'
			return HttpResponse(html)

		if hospital is None:
			html = '<div class="modal-body" id="modal-body-createGroup">Hospital could not be found to edit settings!</div>'
			return HttpResponse(html)

		if request.POST:
			hospitalSettingsForm = PortalHospitalSettingsForm(request.POST)
			settings = None
			if hospitalSettingsForm.is_valid():
				if hospital.hospital_settings is None:
					settings = HospitalSettings()
				else:
					settings = hospital.hospital_settings

				settings.settings_status 		= hospitalSettingsForm.cleaned_data['settings_status']
				settings.settings_email 		= hospitalSettingsForm.cleaned_data['settings_email']
				settings.settings_email_smtp 	= hospitalSettingsForm.cleaned_data['settings_email_smtp']
				settings.settings_video_rate	= hospitalSettingsForm.cleaned_data['settings_video_rate']
				settings.settings_voice_rate	= hospitalSettingsForm.cleaned_data['settings_voice_rate']

				try:
					with transaction.atomic():
						settings.save()
						if hospital.hospital_settings is None:
							hospital.hospital_settings = settings
						hospital.hospital_status = settings.settings_status
						hospital.save()
					return HttpResponseRedirect('/web/'+str(org_id)+'/hospitaldetails/'+str(hospital_id)+'/?setting=updated')
				except:
					traceback.print_exc()
					print '********* form invalid'
					error = 'Error updating settings. Please try again'
					formError = True
					usr_details = request.session['usr_details']
					args['formError'] = formError
					args['error'] = error
					args['usr_details'] = usr_details
					return HttpResponseRedirect('/web/'+str(org_id)+'/hospitaldetails/'+str(hospital_id)+'/?setting=error')

			else:
				print '********form incomplete'
				error = 'Settings form invalid. Please try again!'
				formError = True
				args['formError'] = formError
				args['error'] = error
				args['errorReason'] = hospitalSettingsForm.errors
				return HttpResponseRedirect('/web/'+str(org_id)+'/hospitaldetails/'+str(hospital_id)+'/?setting=incomplete')

		else:
			args['isVoice'] = False
			args['isVideo'] = False
			if hospital.hospital_settings is None:
				hospitalSettingsForm = PortalHospitalSettingsForm()
			else:
				hospitalSettingsForm = PortalHospitalSettingsForm(instance = hospital.hospital_settings)
			if organisation.org_settings.orgsettings_subscription == 'C':
				args['isVoice'] = True
			else:
				args['isVoice'] = True
				args['isVideo'] = True
			args['form'] = hospitalSettingsForm
			args['orgid'] = organisation.org_id
			args['hospitalid'] = hospital.hospital_id
			return render(request,'w_settings_hospital.html',args)

	elif isDoctor:
		doctorSettingsForm = None
		try:
			organisation = Organisation.objects.get(org_id = org_id)
		except:
			html = '<div class="modal-body" id="modal-body-createGroup">Organisation could not be found. Please try again!</div>'
			return HttpResponse(html)
		if organisation.org_id != request.session['org_id']:
			html = '<div class="modal-body" id="modal-body-createGroup">User Not authorized for settings changes for organisation in request!</div>'
			return HttpResponse(html)
		try:
			hospital = Hospital.objects.get( hospital_id = hospital_id,hospital_org = org_id)
		except:
			html = '<div class="modal-body" id="modal-body-createGroup">Hospital could not be found to edit settings!</div>'
			return HttpResponse(html)

		if hospital is None:
			html = '<div class="modal-body" id="modal-body-createGroup">Hospital could not be found to edit settings!</div>'
			return HttpResponse(html)

		try:
			doctor = DoctorRegistration.objects.get(doctor_id = doctor_id, doctor_org = org_id, doctor_hospital = hospital_id)
		except:
			html = '<div class="modal-body" id="modal-body-createGroup">Doctor could not be found to edit settings!</div>'
			return HttpResponse(html)
		if doctor is None:
			html = '<div class="modal-body" id="modal-body-createGroup">Doctor could not be found to edit settings!</div>'
			return HttpResponse(html)

		if request.POST:
			doctorSettingsForm = PortalDoctorSettingsForm(request.POST)
			settings = None
			if doctorSettingsForm.is_valid():
				if doctor.doctor_settings is None:
					settings = DoctorSettings()
				else:
					settings = doctor.doctor_settings
				settings.settings_video 		= doctorSettingsForm.cleaned_data['settings_video']
				settings.settings_voice 		= doctorSettingsForm.cleaned_data['settings_voice']
				settings.settings_eprescription = doctorSettingsForm.cleaned_data['settings_eprescription']
				settings.settings_voice_rate 	= doctorSettingsForm.cleaned_data['settings_voice_rate']
				settings.settings_video_rate 	= doctorSettingsForm.cleaned_data['settings_video_rate']
				settings.settings_status		= doctorSettingsForm.cleaned_data['settings_status']

				try:
					with transaction.atomic():
						settings.save()
						if doctor.doctor_settings is None:
							doctor.doctor_settings = settings
							print(doctor.doctor_settings.settings_id)
						doctor.doctor_status = settings.settings_status
						doctor.save()
					return HttpResponseRedirect('/web/'+str(org_id)+'/doctordetails/'+str(doctor_id)+'/?setting=updated')
				except:
					traceback.print_exc()
					print '********* form invalid'
					error = 'Error updating settings. Please try again'
					formError = True
					args['formError'] = formError
					args['error'] = error
					return HttpResponseRedirect('/web/'+str(org_id)+'/doctordetails/'+str(doctor_id)+'/?setting=error')

			else:
				print '********form incomplete'
				error = 'Settings form invalid. Please try again!'
				formError = True
				args['formError'] = formError
				args['error'] = error
				args['errorReason'] = doctorSettingsForm.errors
				return HttpResponseRedirect('/web/'+str(org_id)+'/doctordetails/'+str(doctor_id)+'/?setting=incomplete')
		else:
			if doctor.doctor_settings is None:
				doctorSettingsForm = PortalDoctorSettingsForm()
			else:
				doctorSettingsForm = PortalDoctorSettingsForm(instance = doctor.doctor_settings)
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
			args['form'] = doctorSettingsForm
			args['orgid'] = organisation.org_id
			args['hospitalid'] = hospital.hospital_id
			args['doctorid'] = doctor.doctor_id
			return render(request,'w_settings_doctor.html',args)
	else:
		html = '<div class="modal-body" id="modal-body-createGroup">Wrong</div>'
		return HttpResponse(html)




""" Ends Settings"""
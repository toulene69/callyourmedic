__author__ = 'apoorv'

from django.http import HttpRequest , HttpResponse , JsonResponse , HttpResponseRedirect , Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.db import IntegrityError, transaction
import traceback

from django.utils import timezone
import pytz, time

# model imports
from models import User
from models import Group
from organisations.models import Organisation, OrgSettings, Apikey
from hospitals.models import Hospital, Department
from doctors.models import DoctorDetails, DoctorRegistration
# form imports
from forms import CYMUserGroupCreationForm
from forms import CYMUserCreationForm, CYMOrgSettingsForm

# utils imports
from utils.session_utils import isUserLogged , userSessionExpired
from utils.app_utils import get_permission , get_active_status
from utils import app_utils
# from cymportal.tasks import mail_to_user
import logging

logger = logging.getLogger('cym')

timezone.activate(pytz.timezone("Asia/Kolkata"))
current_tz = timezone.get_current_timezone()


""" For CYM Users """
def usr_getusers(request):

	res = {
		"draw": 1,
    	"recordsTotal": 0,
    	"recordsFiltered": 0,
		"data" : []
		}
	if request.is_ajax() | True:
		print ("ajax")
		users = list(User.objects.all())
		for user in users:
			usr = {}
			usr['name'] = user.usr_first_name+' '+user.usr_last_name
			usr['username'] = user.usr_email
			usr['phonenumber'] = user.usr_phone
			usr['usergroup'] = user.usr_group.grp_name
			res['data'].append(usr)

		res['recordsTotal'] = len(res['data'])
		res['recordsFiltered'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Users fetch request not proper")

def usr_getgroups(request):
	res = {
		"draw": 1,
    	"recordsTotal": 0,
    	"recordsFiltered": 0,
		"data" : []
		}
	if request.is_ajax() | True:
		print ("ajax")
		x = []
		groups = list(Group.objects.all().order_by('grp_id'))
		i=0
		for group in groups:
			grp = {}
			grp['grpname'] = group.grp_name
			grp['orglevel'] = get_permission(group.grp_org)
			grp['hospitallevel'] = get_permission(group.grp_hospital)
			grp['doclevel'] = get_permission(group.grp_doctor)
			grp['patientlevel'] = get_permission(group.grp_patients)
			grp['calllevel'] = get_permission(group.grp_call)
			grp['transactionlevel'] = get_permission(group.grp_transaction)
			grp['userlevel'] = get_permission(group.grp_user)
			# grp.append('<a href="#">Edit</a>')
			res['data'].append(grp)
		res['recordsTotal'] = len(res['data'])
		res['recordsFiltered'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Groups fetch request not proper")

def usr_usrgroupnew(request):
	error = None
	formError = False
	args = {}
	if isUserLogged(request):
		if request.POST:
			groupCreationForm = CYMUserGroupCreationForm(request.POST)
			if groupCreationForm.is_valid():
				try:
					groupCreationForm.save()
					usr_details = request.session['usr_details']
					args['usr_details'] = usr_details
					return render_to_response('usr_group.html', args)
				except:
					print '********* form invalid'
					error = 'Error creating group. Please try again'
					formError = True
					usr_details = request.session['usr_details']
					args['formError'] = formError
					args['error'] = error
					args['usr_details'] = usr_details
					return render_to_response('usr_group.html', args)

			else:
				print '********form incomplete'
				error = 'Group creation form incomplete. Please try again!'
				formError = True
				usr_details = request.session['usr_details']
				args['formError'] = formError
				args['error'] = error
				args['usr_details'] = usr_details
				return render_to_response('usr_group.html', args)
		else:
			groupCreationForm = CYMUserGroupCreationForm()

		args.update(csrf(request))
		args['groupCreationForm'] = groupCreationForm
		return render_to_response('usr_newgroup.html',args)
	else:
		html = '<div class="modal-body" id="modal-body-createGroup">User Session Expired! <a href="/cymlogin/?sessionError=100">Login</a></div>'
		return HttpResponse(html)

def usr_usernew(request):
	error = None
	formError = False
	args = {}
	if isUserLogged(request):
		if request.POST:
			userCreationForm = CYMUserCreationForm(request.POST)
			if userCreationForm.is_valid():
				try:
					user = User()
					user.usr_first_name = userCreationForm.cleaned_data['usr_first_name']
					user.usr_last_name = userCreationForm.cleaned_data['usr_last_name']
					user.usr_email = userCreationForm.cleaned_data['usr_email']
					user.usr_phone = userCreationForm.cleaned_data['usr_phone']
					user.usr_password = app_utils.generateRandomPassword()
					user.usr_group = userCreationForm.cleaned_data['usr_group']

					user.save()
					# userCreationForm.save()
					usr_details = request.session['usr_details']
					args['usr_details'] = usr_details
					# mail_to_user.delay(user.usr_email,user.usr_password,user.usr_group.grp_name,user.usr_first_name)
					return render_to_response('usr_user.html', args)
				except:
					print '********* form invalid'
					traceback.print_exc()
					error = 'Error creating user. Please try again'
					formError = True
					usr_details = request.session['usr_details']
					args['formError'] = formError
					args['error'] = error
					args['usr_details'] = usr_details
					return render_to_response('usr_user.html', args)

			else:
				print '********* form incomplete'
				error = 'User creation form incomplete. Please try again!'
				formError = True
				usr_details = request.session['usr_details']
				args['formError'] = formError
				args['error'] = error
				args['usr_details'] = usr_details
				return render_to_response('usr_user.html', args)
		else:
			userCreationForm = CYMUserCreationForm()

		args.update(csrf(request))
		args['userCreationForm'] = userCreationForm
		return render_to_response('usr_newuser.html',args)
	else:
		html = '<div class="modal-body" id="modal-body-createGroup">User Session Expired! <a href="/cymlogin/?sessionError=100">Login</a></div>'
		return HttpResponse(html)
""" CYM Users Ends"""

""" For CYM Org """
def org_getorgs(request):

	res = {
		"draw": 1,
    	"recordsTotal": 0,
    	"recordsFiltered": 0,
		"data" : []
		}
	# res = {}
	isMarketPlace = False
	if 'mp' in request.GET:
		try:
			temp = request.GET['mp']
			print(temp)
			if temp == "1":
				isMarketPlace = True
		except:
			traceback.print_exc()
	organisations = None
	if request.is_ajax() | True:
		if isMarketPlace :
			try:
				organisations = list(Organisation.objects.filter(org_settings__in = OrgSettings.objects.filter( orgsettings_marketplace = isMarketPlace)))
			except:
				traceback.print_exc()
		else:
			organisations = list(Organisation.objects.all())
		for organisation in organisations:
			org = {}
			org['name'] = organisation.org_name
			org['brand'] = organisation.org_brand
			org['identifier'] = organisation.org_identifier
			org['state'] = get_active_status(organisation.org_active)
			org['view'] = str(organisation.org_id)
			res['data'].append(org)
		res['recordsTotal'] = len(res['data'])
		res['recordsFiltered'] = len(res['data'])
		return JsonResponse(res )
	else:
		raise Http404("Error in request")

def org_gethospitals(request,org_id=0):
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
			hspt['hospital_name'] = (hospital.hospital_name)
			hspt['branch_code'] = (hospital.hospital_branch_code)
			hspt['city'] = (hospital.hospital_address.address_city)
			hspt['state'] = (hospital.hospital_address.address_state)
			hspt['phone'] = (hospital.hospital_phone1)
			hspt['joined'] = (current_tz.normalize(hospital.hospital_date_joined).date())
			hspt['status'] = hospital.hospital_status
			res['data'].append(hspt)
		res['recordsTotal'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Groups fetch request not proper")

def org_getdoctors(request, org_id=0):
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
				doc['doctor_name'] = (details.doctor_first_name+' '+details.doctor_last_name)
				doc['hospital_branch_code'] = (doctor.doctor_hospital.hospital_branch_code)
				doc['department'] = (doctor.doctor_department.department_name)
				doc['doctor_code'] = (doctor.doctor_code)
				doc['email'] = (doctor.doctor_email)
				if (details.doctor_phone1 is not None):
					doc['phone1'] = str(details.doctor_phone1)
				else:
					doc['phone1'] = "None"
				if (details.doctor_phone2 is not None):
					doc['phone2'] = str(details.doctor_phone2)
				else:
					doc['phone2'] = "None"
				doc['status'] = doctor.doctor_status
				doc['joined'] = details.doctor_date_joined
				#doc.append('<a href="/web/'+ str(org_id) +'/doctordetails/'+ str(doctor.doctor_id) +'">View</a>')
				# doc.append('<a href="#">View</a>')
				res['data'].append(doc)
		except:
			traceback.print_exc()
		res['recordsTotal'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Groups fetch request not proper")


def org_hospital_getdoctors(request,org_id=0,hospital_id=0):
	res = {
    	"recordsTotal": 0,
		"data" : []
		}
	if (org_id ==0 and hospital_id == 0) and (org_id is None or hospital_id is None):
		raise Http404("Groups fetch request not proper")

	if request.is_ajax() | True:
		try:
			doctors = list(DoctorRegistration.objects.filter(doctor_org__exact = org_id, doctor_hospital=hospital_id).order_by('doctor_id'))
			i=0
			for doctor in doctors:
				doc = {}
				details = DoctorDetails.objects.get(doctor_id__exact = doctor.doctor_id)
				doc['doctor_name'] = (details.doctor_first_name+' '+details.doctor_last_name)
				doc['hospital_branch_code'] = (doctor.doctor_hospital.hospital_branch_code)
				doc['department'] = (doctor.doctor_department.department_name)
				doc['doctor_code'] = (doctor.doctor_code)
				doc['email'] = (doctor.doctor_email)
				if (details.doctor_phone1 is not None):
					doc['phone1'] = str(details.doctor_phone1)
				else:
					doc['phone1'] = "None"
				if (details.doctor_phone2 is not None):
					doc['phone2'] = str(details.doctor_phone2)
				else:
					doc['phone2'] = "None"
				doc['status'] = doctor.doctor_status
				doc['joined'] = details.doctor_date_joined
				#doc.append('<a href="/web/'+ str(org_id) +'/doctordetails/'+ str(doctor.doctor_id) +'">View</a>')
				# doc.append('<a href="#">View</a>')
				res['data'].append(doc)
		except:
			traceback.print_exc()
		res['recordsTotal'] = len(res['data'])
		res['recordsFiltered'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Groups fetch request not proper")

""" CYM Ends"""

""" for search drop down """


def org_getorgsforsearch(request):
	res = {
    	"recordsTotal": 0,
		"data" : []
		}
	# res = {}
	if request.is_ajax() | True:
		organisations = list(Organisation.objects.all().values('org_id','org_name'))
		for organisation in organisations:
			org = {}
			org['org_name'] = organisation['org_name']
			org['org_id'] = organisation['org_id']
			res['data'].append(org)
		# res['data'] = organisations
		res['recordsTotal'] = len(res['data'])
		# res['recordsFiltered'] = len(res['data'])
		# res['data'] = organisations
		return JsonResponse(res)
	else:
		raise Http404("Error in request")

def org_gethospitalsforsearch(request,org_id=0):
	res = {
    	"recordsTotal": 0,
		"data" : []
		}
	print(request.GET)
	if request.is_ajax() | True:
		x = []
		hospitals = list(Hospital.objects.filter(hospital_org__exact = org_id).order_by('hospital_id').values('hospital_id','hospital_name'))
		i=0
		for hospital in hospitals:
			hspt = {}
			hspt['hospital_name'] = hospital['hospital_name']
			hspt['hospital_id'] = hospital['hospital_id']
			res['data'].append(hspt)
		res['recordsTotal'] = len(res['data'])
		return JsonResponse(res)
	else:
		raise Http404("Groups fetch request not proper")

def org_getdoctorsforsearch(request,org_id=0,hospital_id=0):
	res = {
    	"recordsTotal": 0,
		"data" : []
		}
	if (org_id ==0 and hospital_id == 0) and (org_id is None or hospital_id is None):
		raise Http404("Groups fetch request not proper")

	if request.is_ajax() | True:
		try:
			doctors = list(DoctorRegistration.objects.filter(doctor_org__exact = org_id, doctor_hospital=hospital_id).order_by('doctor_id'))
			i=0
			for doctor in doctors:
				doc = {}
				details = DoctorDetails.objects.get(doctor_id__exact = doctor.doctor_id)
				doc['doctor_name'] = details.doctor_first_name+' | '+doctor.doctor_code
				doc['doctor_id'] = doctor.doctor_id
				res['data'].append(doc)
		except:
			traceback.print_exc()
		res['recordsTotal'] = len(res['data'])
		return JsonResponse(res)
	else:
		raise Http404("Groups fetch request not proper")

def org_searchdetails(request):
	searchType = None
	args = {}
	try:
		searchType = request.GET['type']
	except:
		args['error'] = "Search type not sent in request"
		return render_to_response('org_search_details.html',args)


	if searchType == 'org':
		args['isSearchOrg'] = True
		try:
			org_id = request.GET['org']
		except:
			args['error'] = "Org ID not sent in request"
			return render_to_response('org_search_details.html',args)

		organisation = None
		department = None
		if org_id != 0:
			orgID = org_id
			try:
				organisation = Organisation.objects.get(org_id = orgID)
				department = Department.objects.filter(department_org = orgID)
			except:
				args['error'] = "Org not found"
				logger.exception("Organisation ID "+str(orgID)+" not found")
				return render_to_response('org_search_details.html',args)
			settings = organisation.org_settings
			apikey = list(Apikey.objects.filter(apikey_org = org_id))
			if settings is not None:
				args['subscription'] = app_utils.get_subscription_type(settings.orgsettings_subscription)
				args['billing_cycle'] = app_utils.get_billing_cycle(settings.orgsettings_billing_cycle)
				args['email']         = settings.orgsettings_email
				args['email_smtp']    = settings.orgsettings_email_smtp
				args['voice_rate']    = settings.orgsettings_voice_rate
				args['video_rate']    = settings.orgsettings_video_rate
				args['subscription_rate'] = settings.orgsettings_subscription_rate
				args['status'] = settings.orgsettings_status
				args['isSettings'] = True
				args['isVoice'] = False
				args['isVideo'] = False
				if organisation.org_settings.orgsettings_subscription == 'C':
					args['isVoice'] = True
				else:
					args['isVoice'] = True
					args['isVideo'] = True
			else:
				args['isSettings'] = False
			if len(apikey) == 0:
				args['apikey'] = None
			else:
				args['apikey'] = apikey[0]
			args['org'] = organisation
			args['depts'] = department
		return render_to_response('org_search_details.html',args)

	elif searchType =='hospital':
		args['isSearchHospital'] = True
		try:
			hospital_id = request.GET['hospital']
		except:
			args['error'] = "Hospital ID not sent in request"
			return render_to_response('org_search_details.html',args)
		hospital = None
		departments = None
		if hospital_id !=0 :
			try:
				hospital = Hospital.objects.get(hospital_id__exact = hospital_id)
				departments = Department.objects.filter(department_id__in =DoctorRegistration.objects.filter(
                            doctor_hospital = hospital_id).values_list('doctor_department', flat=True))
			except:
				args['error'] = "Hospital not found"
				logger.exception("Organisation ID "+str(hospital_id)+" not found")
				return render_to_response('org_search_details.html',args)
			if hospital.hospital_settings is None:
				args['isSettings'] = False
			else:
				settings = hospital.hospital_settings
				args['email']         = settings.settings_email
				args['email_smtp']    = settings.settings_email_smtp
				args['voice_rate']    = settings.settings_voice_rate
				args['video_rate']    = settings.settings_video_rate
				args['status'] 		  = settings.settings_status
				args['isSettings'] = True
			args['depts'] = departments
			args['hospital'] = hospital
		return render_to_response('org_search_details.html',args)

	elif searchType == 'doctor' :
		args['isSearchDoctor'] = True
		try:
			doc_id = request.GET['doctor']
		except :
			args['error'] = "Doctor ID not sent in request"
			return render_to_response('org_search_details.html',args)
		doctor = {}
		docReg = None
		docDetails = None
		try:
			docReg = DoctorRegistration.objects.get( doctor_id = doc_id)
			docDetails = DoctorDetails.objects.get(doctor_id = doc_id)
		except:
			args['error'] = "Doctor details not found"
			return render_to_response('org_search_details.html',args)
		settings = docReg.doctor_settings
		if settings is None:
			args['isSettings'] = False
		else:
			args['isSettings'] = True
			args['isVoice']         = settings.settings_voice
			args['isVideo']         = settings.settings_video
			args['isEprescription'] = settings.settings_eprescription
			args['voice_rate']    	= settings.settings_voice_rate
			args['video_rate']	    = settings.settings_video_rate
			args['status']			= settings.settings_status
		doctor['docReg'] = docReg
		doctor['docDetails'] = docDetails
		args['doctor'] = doctor
		return render_to_response('org_search_details.html',args)
	else :
		args['error'] = "Improper search type"
		return render_to_response('org_search_details.html',args)
	return render_to_response('org_search_details.html',args)

""" Settings """

def org_edit_settings(request,org_id=0):
	error = None
	formError = False
	args = {}
	if isUserLogged(request):
		if org_id == 0:
			html = '<div class="modal-body" id="modal-body-createGroup">Bad Request! Try Again</div>'
			return HttpResponse(html)
		org = Organisation.objects.get(org_id = org_id)
		settings = None
		if request.POST:
			orgSettingsForm = CYMOrgSettingsForm(request.POST)
			if orgSettingsForm.is_valid():
				if org.org_settings is None:
					settings = OrgSettings()
				else:
					settings = org.org_settings
				settings.orgsettings_status = orgSettingsForm.cleaned_data['orgsettings_status']
				settings.orgsettings_billing_cycle = orgSettingsForm.cleaned_data['orgsettings_billing_cycle']
				settings.orgsettings_email = orgSettingsForm.cleaned_data['orgsettings_email']
				settings.orgsettings_email_smtp = orgSettingsForm.cleaned_data['orgsettings_email_smtp']
				settings.orgsettings_subscription = orgSettingsForm.cleaned_data['orgsettings_subscription']
				settings.orgsettings_subscription_rate = orgSettingsForm.cleaned_data['orgsettings_subscription_rate']
				settings.orgsettings_voice_rate = orgSettingsForm.cleaned_data['orgsettings_voice_rate']
				settings.orgsettings_video_rate = orgSettingsForm.cleaned_data['orgsettings_video_rate']
				settings.orgsettings_marketplace = orgSettingsForm.cleaned_data['orgsettings_marketplace']
				org.org_active = orgSettingsForm.cleaned_data['orgsettings_status']
				try:
					with transaction.atomic():
						settings.save()
						if org.org_settings is None:
							org.org_settings = settings
						org.save()
					usr_details = request.session['usr_details']
					return HttpResponseRedirect('/cym/organisationdetails/'+str(org_id)+'/?setting=updated')
				except:
					print '********* form invalid'
					error = 'Error updating settings. Please try again'
					formError = True
					usr_details = request.session['usr_details']
					args['formError'] = formError
					args['error'] = error
					args['usr_details'] = usr_details
					return HttpResponseRedirect('/cym/organisationdetails/'+str(org_id)+'/?setting=error')

			else:
				print '********form incomplete'
				error = 'Settings form incomplete. Please try again!'
				formError = True
				usr_details = request.session['usr_details']
				args['formError'] = formError
				args['error'] = error
				args['usr_details'] = usr_details
				return HttpResponseRedirect('/cym/organisationdetails/'+str(org_id)+'/?setting=incomplete')
		else:
			if org.org_settings is None:
				orgSettingsForm = CYMOrgSettingsForm()
			else:
				orgSettingsForm = CYMOrgSettingsForm(instance = org.org_settings)
		args.update(csrf(request))
		args['orgSettingsForm'] = orgSettingsForm
		args['orgid'] = org_id
		return render_to_response('org_settings_edit.html',args)
	else:
		html = '<div class="modal-body" id="modal-body-createGroup">User Session Expired! <a href="/cymlogin/?sessionError=100">Login</a></div>'
		return HttpResponse(html)
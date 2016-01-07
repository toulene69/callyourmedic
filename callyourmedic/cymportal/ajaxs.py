__author__ = 'apoorv'

from django.http import HttpRequest , HttpResponse , JsonResponse , HttpResponseRedirect , Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
import traceback

from django.utils import timezone
import pytz, time

# model imports
from models import User
from models import Group
from organisations.models import Organisation
from hospitals.models import Hospital
from doctors.models import DoctorDetails, DoctorRegistration
# form imports
from forms import CYMUserGroupCreationForm
from forms import CYMUserCreationForm

# utils imports
from utils.session_utils import isUserLogged , userSessionExpired
from utils.app_utils import get_permission , get_active_status

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
			usr = []
			usr.append(user.usr_first_name+' '+user.usr_last_name)
			usr.append(user.usr_email)
			usr.append(user.usr_phone)
			usr.append(user.usr_group.grp_name)
			res['data'].append(usr)

		res['recordsTotal'] = len(res['data'])
		res['recordsFiltered'] = len(res['data'])
		print res
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
			grp = []
			grp.append(group.grp_name)
			grp.append(get_permission(group.grp_org))
			grp.append(get_permission(group.grp_hospital))
			grp.append(get_permission(group.grp_doctor))
			grp.append(get_permission(group.grp_patients))
			grp.append(get_permission(group.grp_call))
			grp.append(get_permission(group.grp_transaction))
			grp.append(get_permission(group.grp_user))
			grp.append('<a href="#">Edit</a>')
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
					user.usr_password = userCreationForm.cleaned_data['usr_email']
					user.usr_group = userCreationForm.cleaned_data['usr_group']

					user.save()
					# userCreationForm.save()
					usr_details = request.session['usr_details']
					args['usr_details'] = usr_details
					return render_to_response('usr_user.html', args)
				except:
					print '********* form invalid'
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
	if request.is_ajax() | True:
		organisations = list(Organisation.objects.all())
		for organisation in organisations:
			org = []
			org.append(organisation.org_name)
			org.append(organisation.org_brand)
			org.append(organisation.org_identifier)
			org.append(get_active_status(organisation.org_active))
			org.append('<a href="/cym/organisationdetails/'+str(organisation.org_id)+'/">View</a>')
			res['data'].append(org)
		# org = []
		# org.append("XYZ Hospitals Enterprise Ltd.")
		# org.append("XYZ")
		# org.append("123_XYZ")
		# org.append(get_active_status('A'))
		# org.append('<a href="/cym/organisationdetails/'+str(1)+'/">View</a>')
		# res['data'].append(org)
		res['recordsTotal'] = len(res['data'])
		res['recordsFiltered'] = len(res['data'])
		return JsonResponse(res )
	else:
		raise Http404("Error in request")

def org_gethospitals(request,org_id=0):
	res = {
		"draw": 1,
    	"recordsTotal": 0,
    	"recordsFiltered": 0,
		"data" : []
		}
	if request.is_ajax() | True:
		x = []
		hospitals = list(Hospital.objects.filter(hospital_org__exact = org_id).order_by('hospital_id'))
		i=0
		for hospital in hospitals:
			hspt = []
			hspt.append(hospital.hospital_name)
			hspt.append(hospital.hospital_branch_code)
			hspt.append(hospital.hospital_address.address_city)
			hspt.append(hospital.hospital_address.address_state)
			hspt.append(hospital.hospital_phone1)
			hspt.append(current_tz.normalize(hospital.hospital_date_joined).date())
			hspt.append('<a href="#">View</a>')
			res['data'].append(hspt)
		res['recordsTotal'] = len(res['data'])
		res['recordsFiltered'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Groups fetch request not proper")

def org_getdoctors(request, org_id=0):
	res = {
		"draw": 1,
    	"recordsTotal": 0,
    	"recordsFiltered": 0,
		"data" : []
		}
	if request.is_ajax() | True:
		x = []
		try:
			doctors = list(DoctorRegistration.objects.filter(doctor_org__exact = org_id).order_by('doctor_id'))
			i=0
			for doctor in doctors:
				doc = []
				details = DoctorDetails.objects.get(doctor_id__exact = doctor.doctor_id)
				doc.append(details.doctor_first_name+' '+details.doctor_last_name)
				doc.append(doctor.doctor_hospital.hospital_branch_code)
				doc.append(doctor.doctor_department.department_name)
				doc.append(doctor.doctor_code)
				doc.append(doctor.doctor_email)
				doc.append(str(details.doctor_phone1)+'<br>'+str(details.doctor_phone2))
				if doctor.doctor_status:
					doc.append('Active')
				else:
					doc.append('Inactive')
				doc.append(current_tz.normalize(details.doctor_date_joined).date())
				#doc.append('<a href="/web/'+ str(org_id) +'/doctordetails/'+ str(doctor.doctor_id) +'">View</a>')
				doc.append('<a href="#">View</a>')
				res['data'].append(doc)
		except:
			traceback.print_exc()
		res['recordsTotal'] = len(res['data'])
		res['recordsFiltered'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Groups fetch request not proper")

""" CYM Ends"""
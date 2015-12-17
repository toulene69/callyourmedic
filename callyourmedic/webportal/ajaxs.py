__author__ = 'apoorv'

from django.http import HttpRequest , HttpResponse , JsonResponse , HttpResponseRedirect , Http404
from django.shortcuts import render_to_response, render
from django.core.context_processors import csrf
import traceback

from organisations.models import Organisation
from models import WebUser, WebGroup
from hospitals.models import Hospital, Department
from doctors.models import DoctorRegistration, DoctorDetails
# utils imports
from utils.session_utils import isUserLogged , userSessionExpired
from utils.app_utils import get_permission , get_active_status, generateRandomPassword

# form imports
from forms import PortalUserCreationForm, PortalUserGroupCreationForm, PortalDepartmentCreationForm


""" For webportal org"""

def org_getdepartments(request,org_id=0):
	res = {
		"draw": 1,
    	"recordsTotal": 0,
    	"recordsFiltered": 0,
		"data" : []
		}
	if request.is_ajax() | True:
		try:
			departments = list(Department.objects.filter(department_org__exact = org_id))
			for department in departments:
				dept = []
				dept.append(department.department_name)
				dept.append(department.department_description)
				dept.append(department.department_code)
				if department.department_status:
					dept.append('Active')
				else:
					dept.append('Inactive')
				dept.append(department.department_date_added)
				dept.append('<a href="#">Edit</a>')
				res['data'].append(dept)
		except:
			print "error retrieving users"
		res['recordsTotal'] = len(res['data'])
		res['recordsFiltered'] = len(res['data'])
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

""" Ends webportal org"""


""" FOR WebPortal Users"""
def usr_getusers(request,org_id=0):
    res = {
		"draw": 1,
    	"recordsTotal": 0,
    	"recordsFiltered": 0,
		"data" : []
		}
    if request.is_ajax() | True:
        try:
            #organisation = Organisation.objects.get(org_id = org_id)
            users = list(WebUser.objects.filter(usr_org__exact = org_id))
            for user in users:
                usr = []
                usr.append(user.usr_first_name)
                usr.append(user.usr_email)
                usr.append(user.usr_phone)
                usr.append(user.usr_group.grp_name)
                res['data'].append(usr)
        except:
            print "error retrieving users"

        res['recordsTotal'] = len(res['data'])
        res['recordsFiltered'] = len(res['data'])
        return JsonResponse(res , safe = False)
    else:
        raise Http404("Users fetch request not proper")

def usr_getgroups(request,org_id=0):
	res = {
		"draw": 1,
    	"recordsTotal": 0,
    	"recordsFiltered": 0,
		"data" : []
		}
	if request.is_ajax() | True:
		x = []
		groups = list(WebGroup.objects.filter(grp_org_id__exact = org_id).order_by('grp_id'))
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
						groupForm.save()
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
						userForm.usr_password = generateRandomPassword()
						userForm.save()
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
			print(hospitalPresent)
			if len(hospitalPresent) == 0:
				result['present'] = False
	else:
		result['present'] = False
		result['error'] = 'Ajax Error'
	return JsonResponse(result, safe=False)

def hospital_gethospitals(request,org_id=0):
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
			hspt.append(hospital.hospital_date_joined)
			hspt.append('<a href="/web/'+str(org_id)+'/hospitaldetails/'+str(hospital.hospital_id)+'/">View</a>')
			res['data'].append(hspt)
		res['recordsTotal'] = len(res['data'])
		res['recordsFiltered'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Groups fetch request not proper")

""" Ends WebPortal Hospital"""


""" Webportal Doctors"""
def doctor_getdoctors(request, org_id=0):
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
				doc.append(details.doctor_qualification)
				doc.append(details.doctor_experience)
				doc.append(doctor.doctor_email)
				doc.append(str(details.doctor_phone1)+'<br>'+str(details.doctor_phone2))
				doc.append(details.doctor_date_joined)
				doc.append('<a href="#">View</a>')
				res['data'].append(doc)
		except:
			traceback.print_exc()
		res['recordsTotal'] = len(res['data'])
		res['recordsFiltered'] = len(res['data'])
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
				doc = []
				details = DoctorDetails.objects.get(doctor_id__exact = doctor.doctor_id)
				doc.append(details.doctor_first_name+' '+details.doctor_last_name)
				doc.append(doctor.doctor_department.department_name)
				doc.append(doctor.doctor_code)
				doc.append(details.doctor_qualification)
				doc.append(details.doctor_experience)
				doc.append(doctor.doctor_email)
				doc.append(str(details.doctor_phone1)+'<br>'+str(details.doctor_phone2))
				doc.append(details.doctor_date_joined)
				doc.append('<a href="#">View</a>')
				res['data'].append(doc)
		except:
			traceback.print_exc()
		res['recordsTotal'] = len(res['data'])
		res['recordsFiltered'] = len(res['data'])
		return JsonResponse(res , safe = False)
	else:
		raise Http404("Groups fetch request not proper")


""" Ends Webportal doctors"""
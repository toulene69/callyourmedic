__author__ = 'apoorv'

from django.conf.urls import include, url

urlpatterns = [

    url(r'^dashboard/', 'webportal.views.dashboard'),

    # webportal Org
    url(r'^org/', 'webportal.views.org_dashboard'),
    url(r'^departments/', 'webportal.views.org_departments'),

    # webportal hospital
    url(r'^hospital/', 'webportal.views.hospital_dashboard'),
    url(r'^(?P<org_id>\d+)/hospitaldetails/(?P<hospital_id>\d+)/$', 'webportal.views.hospital_details'),
    url(r'^(?P<org_id>\d+)/hospitaldetails/$', 'webportal.views.hospital_details'),
    url(r'^(?P<org_id>\d+)/hospitalnew/$', 'webportal.views.hospital_new'),

    # webportal doctors
    url(r'^doctors/', 'webportal.views.doctor_dashboard'),
    url(r'^(?P<org_id>\d+)/doctornew/$', 'webportal.views.doctor_new'),
    url(r'^(?P<org_id>\d+)/doctordetails/(?P<doctor_id>\d+)/$', 'webportal.views.doctor_details'),
    url(r'^(?P<org_id>\d+)/doctordetails/$', 'webportal.views.doctor_details'),

    # webportal users

    url(r'^usr/', 'webportal.views.usr_dashboard'),
    url(r'^users/', 'webportal.views.usr_users'),
    url(r'^usrgroup/', 'webportal.views.usr_group'),


    # ajax calls
    url(r'^(?P<org_id>\d+)/getusers/', 'webportal.ajaxs.usr_getusers',name = 'get-users'),
    url(r'^(?P<org_id>\d+)/getgroups/', 'webportal.ajaxs.usr_getgroups',name = 'get-groups'),
    url(r'^(?P<org_id>\d+)/usrgroupnew/', 'webportal.ajaxs.usr_usrgroupnew',name = 'get-usrgroupnew'),
    url(r'^(?P<org_id>\d+)/usrnew/', 'webportal.ajaxs.usr_usernew',name = 'get-usrnew'),
    url(r'^(?P<org_id>\d+)/branchcode/', 'webportal.ajaxs.hospital_check_branch_code',name = 'check-hospitalcode'),
    url(r'^(?P<org_id>\d+)/gethospitals/', 'webportal.ajaxs.hospital_gethospitals',name = 'get-hospitals'),
    url(r'^(?P<org_id>\d+)/getdepartments/', 'webportal.ajaxs.org_getdepartments',name = 'get-departments'),
    url(r'^(?P<org_id>\d+)/departmentnew/', 'webportal.ajaxs.org_departmentnew',name = 'get-departmentnew'),
    url(r'^(?P<org_id>\d+)/getdoctors/', 'webportal.ajaxs.doctor_getdoctors',name = 'get-doctors'),
    url(r'^(?P<org_id>\d+)/hospital/(?P<hospital_id>\d+)/getdoctors/', 'webportal.ajaxs.doctor_getdoctorsforhospitals',name = 'get-hospital-doctors'),

    url(r'^orgsettings/(?P<org_id>\d+)/', 'webportal.ajaxs.settings_edit',name = 'org-settings'),
    url(r'^hospitalsettings/(?P<org_id>\d+)/(?P<hospital_id>\d+)/', 'webportal.ajaxs.settings_edit',name = 'hospital-settings'),
    url(r'^doctorsettings/(?P<org_id>\d+)/(?P<hospital_id>\d+)/(?P<doctor_id>\d+)/', 'webportal.ajaxs.settings_edit',name = 'doctor-settings'),

    url(r'^(?P<org_id>\d+)/departmentedit/(?P<dept_id>\d+)/', 'webportal.ajaxs.org_departmentedit',name = 'org-departmentedit'),
    url(r'^(?P<org_id>\d+)/groupedit/(?P<grp_id>\d+)/', 'webportal.ajaxs.usr_groupedit',name = 'usr-groupedit'),
]

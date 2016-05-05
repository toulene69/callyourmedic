__author__ = 'apoorv'

from django.conf.urls import include, url

urlpatterns = [
    #url(r'^', 'cymportal.views.login'),
    url(r'^login/', 'cymportal.views.login'),
    url(r'^dashboard/', 'cymportal.views.dashboard'),

    # cym org
    url(r'^organisation/', 'cymportal.views.org_dashboard'),
    url(r'^organisationdetails/$', 'cymportal.views.org_details'),

    url(r'^organisationdetails/(?P<org_id>\d+)/$', 'cymportal.views.org_details'),
    url(r'^search/$','cymportal.views.search'),
    url(r'^(?P<org_id>\d+)/hospitaldetails/$','cymportal.views.org_hospital_details'),
    url(r'^(?P<org_id>\d+)/hospitaldetails/(?P<hospital_id>\d+)/$','cymportal.views.org_hospital_details'),

    url(r'^organisationnew/', 'cymportal.views.org_new'),
    url(r'^organisationrequests/$', 'cymportal.views.org_requests'),
    url(r'^organisationrequests/(?P<org_id>\d+)/$', 'cymportal.views.org_requests'),
    url(r'^generateapikey/(?P<org_id>\d+)/','cymportal.views.org_create_apikey'),

    #cym marketplace
    url(r'^marketplace/', 'cymportal.views.mp_dashboard'),
    url(r'^mp/generateapikey/','cymportal.views.mp_generateapikey'),

    #cym user
    url(r'^usr/', 'cymportal.views.usr_dashboard'),
    url(r'^users/', 'cymportal.views.usr_users'),
    url(r'^usrgroup/$', 'cymportal.views.usr_group'),

    #cym ajax
    url(r'^getusers/', 'cymportal.ajaxs.usr_getusers',name = 'get-users'),
    url(r'^usrnew/', 'cymportal.ajaxs.usr_usernew',name = 'get-usrnew'),
    url(r'^getgroups/', 'cymportal.ajaxs.usr_getgroups',name = 'get-groups'),
    url(r'^usrgroupnew/', 'cymportal.ajaxs.usr_usrgroupnew',name = 'get-usrgroupnew'),
    url(r'^getorgs/', 'cymportal.ajaxs.org_getorgs',name = 'get-orgs'),
    url(r'^(?P<org_id>\d+)/gethospitals/', 'cymportal.ajaxs.org_gethospitals',name = 'get-hospitals'),
    url(r'^(?P<org_id>\d+)/getdoctors/', 'cymportal.ajaxs.org_getdoctors',name = 'get-doctors'),
    url(r'^(?P<org_id>\d+)/(?P<hospital_id>\d+)/getdoctors/', 'cymportal.ajaxs.org_hospital_getdoctors',name = 'get-doctorsForHospital'),

    url(r'^getorgsforsearch/', 'cymportal.ajaxs.org_getorgsforsearch'),
    url(r'^(?P<org_id>\d+)/gethospitalsforsearch/', 'cymportal.ajaxs.org_gethospitalsforsearch'),
    url(r'^(?P<org_id>\d+)/(?P<hospital_id>\d+)/getdoctorsforsearch/', 'cymportal.ajaxs.org_getdoctorsforsearch'),
    url(r'^getsearchdetails/', 'cymportal.ajaxs.org_searchdetails'),

    #edit settings
    url(r'^(?P<org_id>\d+)/orgsettings/', 'cymportal.ajaxs.org_edit_settings'),
]

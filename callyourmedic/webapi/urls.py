__author__ = 'apoorv'


from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
import views

urlpatterns = [
    url(r'^patient/', 'webapi.views.patient'),
    url(r'^login/', 'webapi.views.login'),
    url(r'^logout/', 'webapi.views.logout'),
    url(r'^changepassword/', 'webapi.views.passwordchange'),
    # url(r'^departments/', views.DepartmentList.as_view()),
    url(r'^orgs/', 'webapi.views.orgs'),
    url(r'^departments/', 'webapi.views.departments'),
    url(r'^doctors/', 'webapi.views.doctors'),

    #url(r'^doctors/', views.DoctorList.as_view()),
    url(r'^telephony/', 'webapi.telephony.callback'),
    url(r'^call/', 'webapi.telephony.webcall'),
]


urlpatterns = format_suffix_patterns(urlpatterns)

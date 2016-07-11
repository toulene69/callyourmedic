__author__ = 'apoorv'

from django.http import HttpRequest
from django.http import HttpResponseRedirect

import logging

logger = logging.getLogger(__name__)

def isUserLogged(request):
    if 'usr_id' in request.session:
        return True
    else :
        return False

def createUserSession(request,user):
    usr_details = {
        'first_name' : user.usr_first_name,
        'group_id' : user.usr_group_id,
    }
    request.session['usr_id'] = user.usr_id
    request.session['usr_details'] = usr_details
    if request.session.test_cookie_worked():
        request.session['isCookieEnables'] = True
        request.session.delete_test_cookie()
    else:
        request.session['isCookieEnables'] = False
    request.session.set_expiry(1800)

def destroyUserSession(request):
    if 'usr_id' in request.session :
        del request.session['usr_id']

    request.session.flush()

    request.session.clear_expired()

def userSessionExpired():
	return HttpResponseRedirect('/cymlogin/?' + 'sessionError=100')
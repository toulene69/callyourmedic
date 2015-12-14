__author__ = 'apoorv'

from django.http import HttpRequest
from django.http import HttpResponseRedirect

import logging

logger = logging.getLogger(__name__)

def isUserLogged(request):
    if 'usr_id' in request.session:
        print ('******** User Already Logged in ')
        return True
    else :
        print ('******** User Not Already Logged in ')
        return False

def createUserSession(request,user):
    print ('******** Session creating  ')
    usr_details = {
        'first_name' : user.usr_first_name,
        'group_id' : user.usr_group_id,
    }
    request.session['usr_id'] = user.usr_id
    request.session['usr_details'] = usr_details
    if request.session.test_cookie_worked():
        request.session['isCookieEnables'] = True
    else:
        request.session['isCookieEnables'] = False
    request.session.delete_test_cookie()
    request.session.set_expiry(1800)
    print ('******** Session created : ')
    print(request.session['usr_id'])

def destroyUserSession(request):
    print ('******** Session deleting : ')
    if 'usr_id' in request.session :
        del request.session['usr_id']
    else:
        print ('***** session expired')
    request.session.flush()
    print ('******** Session deleted ')
    request.session.clear_expired()

def userSessionExpired():
	return HttpResponseRedirect('/cymlogin/?' + 'sessionError=100')
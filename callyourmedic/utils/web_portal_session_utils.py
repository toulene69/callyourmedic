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
    print ('******** Session creating  ')
    usr_details = {
        'first_name' : user.usr_first_name,
        'group_id' : user.usr_group_id,
    }
    request.session['org_id'] = user.usr_org.org_id
    request.session['org_name'] = user.usr_org.org_name
    request.session['usr_id'] = user.usr_id
    request.session['usr_details'] = usr_details
    if request.session.test_cookie_worked():
        request.session['isCookieEnables'] = True
    else:
        request.session['isCookieEnables'] = False
    request.session.delete_test_cookie()
    request.session.set_expiry(1800)


def destroyUserSession(request):
    if 'usr_id' in request.session :
        del request.session['usr_id']
    else:
        print ('***** session expired')
    request.session.flush()
    request.session.clear_expired()

def userSessionExpired():
	return HttpResponseRedirect('/portal/?' + 'sessionError=100')

def isUserRequestValid(request,org_id):
    if 'org_id' in request.session:
        id = int(request.session['org_id'])
        if (id == int(org_id)):
            return True
        else:
            return False
    else:
        return userSessionExpired()
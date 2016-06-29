__author__ = 'apoorv'

from django.utils import timezone
import os
import sys
import random
import string
import django.contrib.auth.hashers
from django.contrib.auth.hashers import make_password, get_hasher, check_password

# Consider adding string.punctuation

import string, time, math, random

def uniqid(prefix='', more_entropy=False):
    m = time.time()
    uniqid = '%8x%05x' %(math.floor(m),(m-math.floor(m))*1000000)
    if more_entropy:
        valid_chars = list(set(string.hexdigits.lower()))
        entropy_string = ''
        for i in range(0,10,1):
            entropy_string += random.choice(valid_chars)
        uniqid = uniqid + entropy_string
    uniqid = prefix + uniqid
    return uniqid

def date_default():
    return timezone.now()


def choices_gender():
    GENDER_VALUE = (
        ('M','Male'),
        ('F','Female'),
    )
    return GENDER_VALUE

def choices_user_permissions():
    PERMISSION = (
        (0,'No Access'),
        (1,'Read Only'),
        (2,'Read Write'),
    )
    return PERMISSION

def get_permission(value):
    if value==0:
        return 'No Access'
    elif value==1:
        return 'Read Only'
    else:
        return 'Read Write'

def choices_active_status():
    ORG_ACTIVE_STATUS = (
        ('A','Active'),
        ('D','Dead'),
        ('T','Test'),
    )
    return ORG_ACTIVE_STATUS

def get_active_status(value):
    if value=='A':
        return 'Active'
    elif value=='D':
        return 'Dead'
    else:
        return 'Test'

SUBSCRIPTION_TYPE = (
        ('C', 'Call Only Consultation'),
        ('CV', 'Call and Video Consultation'),
        ('CVP', 'Call and Video with e-Prescription')
    )

BILLING_CYCLE = (
        (1, 'Daily'),
        (7, 'Weekly'),
        (14, 'Bi-Weekly'),
        (30, 'Monthly')
    )

def choice_subscription_type():

    return SUBSCRIPTION_TYPE

def get_subscription_type(value):
    if value == 'C':
        return 'Call Only Consultation'
    elif value == 'CV':
        return 'Call and Video Consultation'
    elif value == 'CVP' :
        return 'Call and Video with e-Prescription'
    else:
        return None

def choice_billing_cycle():

    return BILLING_CYCLE

def get_billing_cycle(value):
    if value == 1:
        return 'Daily'
    elif value == 7:
        return 'Weekly'
    elif value == 14:
        return 'Bi-Weekly'
    elif value == 30:
        return 'Monthly'
    else :
        return '-NA-'

def generateRandomPassword():
    CHAR_LIST = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
    PASSWORD_LENGTH = 8
    password = ''
    rnd = random.SystemRandom()
    for i in range(0,8,1):
        index = rnd.randint(0,60)
        password += CHAR_LIST[index]
    print 'Password created: '+password
    return password

def generateDoctorCode(org_id,hospital_code,doc_id):
    docCode = str(org_id)+'_'+hospital_code+'_'+str(doc_id)
    docCode = docCode.replace(" ", "")
    return docCode


def generateAPIKey():
    CHAR_LIST = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
    PASSWORD_LENGTH = 16
    key = ''
    rnd = random.SystemRandom()
    for i in range(0,16,1):
        index = rnd.randint(0,60)
        key += CHAR_LIST[index]
    print 'apikey created: '+key
    return key

def generateAuthToken(length=64):
    possible_characters = string.ascii_letters + string.digits
    rng = random.SystemRandom()
    tok = ""
    tok = tok.join([rng.choice(possible_characters) for i in range(length)])
    return tok

def getPasswordHash(password):
    if password is None :
        return None
    else:
        hasher = get_hasher('default')
        salt = hasher.salt()
        pass_hash = make_password(password,salt)
        return pass_hash

def checkPassword(password,hash):
    if password is None:
        return False
    if password == hash:
        return True
    if check_password(password,hash) :
        return True
    else:
        return False

__author__ = 'apoorv'

from django.utils import timezone
import os
import sys
import random
import string
import django.contrib.auth.hashers
from django.contrib.auth.hashers import make_password, get_hasher, check_password

# Consider adding string.punctuation

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
    docCode = str(org_id)+'#'+hospital_code+'#'+str(doc_id)
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
    if check_password(password,hash) :
        return True
    else:
        return False
from django.db import models
from django.db import IntegrityError, transaction
import traceback

from utils.app_utils import choices_user_permissions, generateRandomPassword
from organisations.models import Organisation
from mailer.views import *
from utils.app_utils import get_permission, getPasswordHash
from hospitals.models import Hospital
# web portal users and user groups



class WebGroup(models.Model):

    grp_id          = models.AutoField(primary_key = True)
    grp_name        = models.CharField(max_length = 50,blank = False)
    grp_org_id      = models.ForeignKey(Organisation)
    grp_org         = models.PositiveIntegerField(blank = False, choices = choices_user_permissions())
    grp_hospital    = models.PositiveIntegerField(blank = False, choices = choices_user_permissions())
    grp_doctor      = models.PositiveIntegerField(blank = False, choices = choices_user_permissions())
    grp_patients    = models.PositiveIntegerField(blank = False, choices = choices_user_permissions())
    grp_call        = models.PositiveIntegerField(blank = False, choices = choices_user_permissions())
    grp_transaction = models.PositiveIntegerField(blank = False, choices = choices_user_permissions())
    grp_user        = models.PositiveIntegerField(blank = False, choices = choices_user_permissions())
    grp_status      = models.BooleanField(default = True)
    is_super        = models.BooleanField(default = False)
    def __str__(self): # __unicode__ on Python 2
        return self.grp_name


class WebUser(models.Model):

    usr_id          = models.AutoField(primary_key = True)
    usr_org         = models.ForeignKey(Organisation)
    usr_first_name  = models.CharField(max_length = 100, blank = False)
    usr_last_name   = models.CharField(max_length = 100,blank = True)
    usr_email       = models.EmailField(blank = False)
    usr_phone       = models.CharField(max_length = 11,blank = True)
    usr_password    = models.CharField(max_length = 130, null = False, blank = False)
    usr_group       = models.ForeignKey(WebGroup)
    usr_status      = models.BooleanField(default = True)
    def __str__(self): # __unicode__ on Python 2
        return self.usr_first_name


def createSuperUserAndGroup(emailid,phonenumber,org,usr_first_name,org_identifier):
    superadmin = WebGroup()
    superadmin.grp_name = 'Org Super Admin'
    superadmin.grp_org_id = org
    superadmin.grp_hospital = 2
    superadmin.grp_doctor = 2
    superadmin.grp_org = 2
    superadmin.grp_patients = 2
    superadmin.grp_call = 2
    superadmin.grp_transaction = 2
    superadmin.grp_user = 2
    superadmin.is_super = True

    superuser = WebUser()
    superuser.usr_email = emailid
    randomPassword = generateRandomPassword()
    superuser.usr_password = getPasswordHash(randomPassword)
    superuser.usr_phone = phonenumber
    superuser.usr_first_name = 'Super Admin'
    superuser.usr_org = org
    try:
        with transaction.atomic():
            superadmin.save()
            superuser.usr_group = superadmin
            superuser.save()
        send_mail_for_group(superuser.usr_email,superadmin)
        send_mail_for_super_user(superuser,randomPassword,org_identifier)
        return True
    except:
        return False


def send_mail_for_group(email,superadmin):
    mail_dict = MAIL_DATA_DICT
    # MAIL_DATA_DICT = {
    #  	TYPE : None,
    #  	TO : None,
    #  	CC : None,
    #  	BCC : None,
    #  	FROM : None,
    #  	MESSAGE : None,
    #  	DETAILS : None
    #  }
    mail_dict[TYPE] = MAIL_PORTAL_GROUP
    mail_dict[TO] = [email]
    grp = {}
    grp['Group Name'] = superadmin.grp_name
    grp['Org level'] = get_permission(superadmin.grp_org)
    grp['Hospital level'] = get_permission(superadmin.grp_hospital)
    grp['Doctor level'] = get_permission(superadmin.grp_doctor)
    grp['Patient level'] = get_permission(superadmin.grp_patients)
    grp['Call level'] = get_permission(superadmin.grp_call)
    grp['Transaction level'] = get_permission(superadmin.grp_transaction)
    grp['User level'] = get_permission(superadmin.grp_user)
    mail_dict[DETAILS] = grp
    mailer = EmailHandler(mail_dict)
    logger.info("Sending mail org admin for Super Admin group creation")
    mailer.send_mail()

def send_mail_for_super_user(superuser,randomPassword,org_identifier):
    mail_dict = MAIL_DATA_DICT
    # MAIL_DATA_DICT = {
    #  	TYPE : None,
    #  	TO : None,
    #  	CC : None,
    #  	BCC : None,
    #  	FROM : None,
    #  	MESSAGE : None,
    #  	DETAILS : None
    #  }
    mail_dict[TYPE] = MAIL_PORTAL_USER
    mail_dict[TO] = [superuser.usr_email]
    grp = {}
    grp['Name'] = superuser.usr_first_name
    grp['User Name'] = superuser.usr_email
    grp['Password'] = randomPassword
    grp['Org Identifier'] = org_identifier
    mail_dict[DETAILS] = grp
    mailer = EmailHandler(mail_dict)
    logger.info("Sending mail org admin for Super Admin creation")
    mailer.send_mail()
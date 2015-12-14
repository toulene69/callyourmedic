from django.db import models

from utils.app_utils import choices_user_permissions, generateRandomPassword
from organisations.models import Organisation
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
    def __str__(self): # __unicode__ on Python 2
        return self.grp_name


class WebUser(models.Model):

    usr_id          = models.AutoField(primary_key = True)
    usr_org         = models.ForeignKey(Organisation)
    usr_first_name  = models.CharField(max_length = 100, blank = False)
    usr_last_name   = models.CharField(max_length = 100,blank = True)
    usr_email       = models.EmailField(blank = False)
    usr_phone       = models.CharField(max_length = 11,blank = True)
    usr_password    = models.CharField(max_length = 20,blank = True)
    usr_group       = models.ForeignKey(WebGroup)
    usr_status      = models.BooleanField(default = True)
    def __str__(self): # __unicode__ on Python 2
        return self.usr_first_name


def createSuperUserAndGroup(emailid,phonenumber,org,usr_first_name):
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

    superuser = WebUser()
    superuser.usr_email = emailid
    superuser.usr_password = generateRandomPassword()
    superuser.usr_phone = phonenumber
    superuser.usr_first_name = 'Super Admin'
    superuser.usr_org = org
    try:
        superadmin.save()
        superuser.usr_group = superadmin
        superuser.save()
        return True
    except:
        return False
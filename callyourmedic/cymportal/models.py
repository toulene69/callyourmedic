from django.db import models
from utils import app_utils

# cym portal users and user groups



class Group(models.Model):

    grp_id          = models.AutoField(primary_key = True)
    grp_name        = models.CharField(max_length = 50,blank = False)
    grp_org         = models.PositiveIntegerField(blank = False, choices = app_utils.choices_user_permissions())
    grp_hospital    = models.PositiveIntegerField(blank = False, choices = app_utils.choices_user_permissions())
    grp_doctor      = models.PositiveIntegerField(blank = False, choices = app_utils.choices_user_permissions())
    grp_patients    = models.PositiveIntegerField(blank = False, choices = app_utils.choices_user_permissions())
    grp_call        = models.PositiveIntegerField(blank = False, choices = app_utils.choices_user_permissions())
    grp_transaction = models.PositiveIntegerField(blank = False, choices = app_utils.choices_user_permissions())
    grp_user        = models.PositiveIntegerField(blank = False, choices = app_utils.choices_user_permissions())

    def __str__(self): # __unicode__ on Python 2
        return self.grp_name


class User(models.Model):

    usr_id          = models.AutoField(primary_key = True)
    usr_first_name  = models.CharField(max_length = 100, blank = False)
    usr_last_name   = models.CharField(max_length = 100,blank = True)
    usr_email       = models.EmailField(blank = False,unique = True)
    usr_phone       = models.CharField(max_length = 11,blank = True)
    usr_password    = models.CharField(max_length = 20,blank = True)
    usr_group       = models.ForeignKey(Group)

    def __str__(self): # __unicode__ on Python 2
        return self.usr_first_name



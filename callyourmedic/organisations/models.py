from django.db import models
from utils import app_utils

from addresses.models import Address

class OrgSettings(models.Model):

    orgsettings_id            = models.AutoField(primary_key = True)
    orgsettings_subscription  = models.CharField(max_length = 5, default = 'C' , choices = app_utils.choice_subscription_type())
    orgsettings_billing_cycle = models.PositiveIntegerField(default = 30,choices = app_utils.choice_billing_cycle())
    orgsettings_email         = models.EmailField(help_text = "This email will be used to send the auto generated mails to the general customers.", null = True, blank = True, default = None)
    orgsettings_email_smtp    = models.CharField(max_length = 20, null = True, blank = True, default = None)
    orgsettings_voice_rate    = models.DecimalField( max_digits=7, decimal_places=2, null = True, blank = True , default = None)
    orgsettings_video_rate    = models.DecimalField( max_digits=7, decimal_places=2, null = True, blank = True , default = None)
    orgsettings_subscription_rate = models.DecimalField( max_digits=7, decimal_places=2, null = True, blank = True , default = None)
    orgsettings_status        = models.CharField(max_length = 1, choices = app_utils.choices_active_status())

    def __str__(self): # __unicode__ on Python 2
        return app_utils(self.orgsettings_subscription)

# Organisation model
class Organisation(models.Model):
    ORG_ACTIVE_STATUS = (
        ('A','Active'),
        ('D','Dead'),
        ('T','Test'),
    )

    org_id           = models.AutoField(primary_key = True)
    org_name         = models.CharField(max_length = 300, blank = False)
    org_brand        = models.CharField(max_length = 200)
    org_identifier   = models.CharField(max_length = 20, unique = True)
    org_emailid      = models.EmailField()
    org_phone        = models.CharField(max_length = 11,blank = True)
    org_active       = models.CharField(max_length = 1, choices = app_utils.choices_active_status())
    org_address      = models.ForeignKey(Address)
    org_date_joined  = models.DateTimeField(default = app_utils.date_default())
    org_date_left    = models.DateTimeField(null = True)
    org_billing_id   = models.CharField(max_length = 100)         # concatenation of the orgid and org identifier
    org_settings     = models.OneToOneField(OrgSettings, null = True )

    def __str__(self): # __unicode__ on Python 2
        return self.org_name

# api key model
class Apikey(models.Model):

    apikey_id               = models.AutoField(primary_key = True)
    apikey_org              = models.ForeignKey(Organisation)
    apikey_key              = models.CharField(max_length=17,unique = True)
    apikey_status           = models.BooleanField(default = True)
    apikey_generation_date  = models.DateTimeField(default = app_utils.date_default())
    apikey_termination_date = models.DateTimeField(null = True)








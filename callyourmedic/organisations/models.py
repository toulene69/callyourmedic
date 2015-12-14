from django.db import models
from utils import app_utils

from addresses.models import Address

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

    def __str__(self): # __unicode__ on Python 2
        return self.org_name

# api key model
class Apikey(models.Model):

    apikey_id               = models.AutoField(primary_key = True)
    apikey_org              = models.ForeignKey(Organisation)
    apikey_key              = models.PositiveIntegerField()
    apikey_status           = models.BooleanField()
    apikey_generation_date  = models.DateTimeField()
    apikey_termination_date = models.DateTimeField()



# Organisation and hospital level user model




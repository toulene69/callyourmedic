from django.db import models
from utils import app_utils
from organisations.models import Organisation
from addresses.models import Address

# hospital model
class Hospital(models.Model):

    hospital_id              = models.AutoField(primary_key = True)
    hospital_org             = models.ForeignKey(Organisation)
    hospital_name            = models.CharField(max_length = 200)
    hospital_branch_code     = models.CharField(max_length = 50)
    hospital_address         = models.ForeignKey(Address)
    hospital_email_id        = models.EmailField()
    hospital_phone1          = models.PositiveIntegerField()
    hospital_phone2          = models.PositiveIntegerField(null = True)
    hospital_status          = models.BooleanField(default=True)
    hospital_date_joined     = models.DateTimeField(default = app_utils.date_default())
    hospital_date_left       = models.DateTimeField(null=True)

    def __str__(self): # __unicode__ on Python 2
        return self.hospital_name

# department model for hospitals
class Department(models.Model):


    department_id           = models.AutoField(primary_key = True)
    department_org          = models.ForeignKey(Organisation)
    department_name         = models.CharField(max_length = 100)
    department_description  = models.CharField(max_length = 200, null = True)
    department_code         = models.CharField(max_length = 10)
    department_status       = models.BooleanField(default = True)
    department_date_added   = models.DateTimeField(default = app_utils.date_default())

    def __str__(self): # __unicode__ on Python 2
        return self.department_name
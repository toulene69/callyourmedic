from django.db import models

from utils import app_utils
from addresses.models import Address
from organisations.models import Organisation

class Patients(models.Model):

    patient_id          = models.AutoField(primary_key = True)
    patient_org         = models.ForeignKey(Organisation)
    patient_first_name  = models.CharField(max_length = 100)
    patient_last_name   = models.CharField(max_length = 100)
    patient_dob         = models.DateTimeField()
    patient_date_joined = models.DateTimeField(app_utils.date_default())
    patient_date_left   = models.DateTimeField()
    patient_gender      = models.CharField(max_length = 1, choices = app_utils.choices_gender())
    patient_email       = models.EmailField()
    patient_phone1      = models.PositiveIntegerField()
    patient_phone2      = models.PositiveIntegerField(null = True)
    patient_address     = models.ForeignKey(Address)
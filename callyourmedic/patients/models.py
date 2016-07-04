from django.db import models
from django.contrib import auth

from utils import app_utils
from addresses.models import Address
from organisations.models import Organisation
from mailer.views import *

import logging
logger = logging.getLogger('webapi')

class Patients(models.Model):

    patient_id          = models.AutoField(primary_key = True)
    patient_org         = models.ForeignKey(Organisation, null = True, blank = True)
    patient_first_name  = models.CharField(max_length = 100,blank = True)
    patient_last_name   = models.CharField(max_length = 100, blank = True)
    patient_dob         = models.DateField(null = True)
    patient_date_joined = models.DateTimeField(default = app_utils.date_default())
    patient_date_left   = models.DateTimeField(null = True)
    patient_gender      = models.CharField(max_length = 1, choices = app_utils.choices_gender(),blank = True)
    patient_email       = models.EmailField(null = False, blank = False)
    patient_phone1      = models.CharField(max_length = 15, null = False, blank = False)
    patient_password    = models.CharField(max_length = 130, null = False, blank = False)
    patient_address     = models.ForeignKey(Address,blank=True,null=True,)
    patient_ismarketplace = models.BooleanField(default = False)

    def __str__(self): # __unicode__ on Python 2
        return self.patient_email

class PatientAuthToken(models.Model):
    patient          = models.ForeignKey(Patients, unique = True)
    patient_token    = models.CharField(max_length = 64, blank = True, null = True)



def mail_to_send_patient(patient):
    """
        Parameters : doctor, random passwrod, org_identifier
    """
    if patient is None:
        return
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
    mail_dict[TYPE] = MAIL_PORTAL_PATIENT
    mail_dict[TO] = [patient.patient_email]
    mailer = EmailHandler(mail_dict)
    logger.info("Sending mail for patient creation")
    mailer.send_mail()
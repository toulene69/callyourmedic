from django.db import models

from utils import app_utils
from organisations.models import Organisation
from hospitals.models import Hospital
from hospitals.models import Department
from addresses.models import Address
from mailer.views import *

import logging
logger = logging.getLogger('webportal')

class DoctorSettings(models.Model):

    settings_id            = models.AutoField(primary_key = True)
    settings_voice         = models.BooleanField(default = False)
    settings_video         = models.BooleanField(default = False)
    settings_eprescription = models.BooleanField(default = False)
    settings_voice_rate    = models.DecimalField( max_digits=7, decimal_places=2, null = True, blank = True)
    settings_video_rate    = models.DecimalField( max_digits=7, decimal_places=2, null = True, blank = True)
    settings_status        = models.BooleanField(default = True)

class DoctorRegistration(models.Model):

    doctor_id          = models.AutoField(primary_key = True)
    doctor_org         = models.ForeignKey(Organisation)
    doctor_hospital    = models.ForeignKey(Hospital)
    doctor_department  = models.ForeignKey(Department)
    doctor_email       = models.EmailField()
    doctor_password    = models.CharField(max_length = 130, null = False, blank = False)
    doctor_status      = models.BooleanField(default = True)
    doctor_code        = models.CharField(max_length = 50)
    doctor_settings    = models.OneToOneField(DoctorSettings, null = True)



class DoctorDetails(models.Model):

    info_id            = models.AutoField(primary_key = True)
    doctor_id          = models.ForeignKey(DoctorRegistration,db_column = 'doctor_id')
    doctor_first_name  = models.CharField(max_length = 100)
    doctor_last_name   = models.CharField(max_length = 100)
    doctor_gender      = models.CharField(max_length = 1, choices = app_utils.choices_gender())
    doctor_phone1      = models.CharField(max_length = 30,blank = True)
    doctor_phone2      = models.CharField(max_length = 30,blank = True, null = True)
    doctor_qualification = models.CharField(max_length = 400)
    doctor_experience   = models.PositiveIntegerField(default = 0)
    doctor_address     = models.ForeignKey(Address)
    doctor_date_joined = models.DateTimeField(default=app_utils.date_default())
    doctor_date_left   = models.DateTimeField(blank=True, null=True)


    def __str__(self): # __unicode__ on Python 2
        return self.doctor_first_name


def send_mail_to_doctor(doctor,randomPassword,org_identifier):
    """
        Parameters : doctor, random passwrod, org_identifier
    """
    if doctor is None:
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
    mail_dict[TYPE] = MAIL_PORTAL_DOCTOR
    mail_dict[TO] = [doctor.doctor_email]
    doc = {}
    doc['User Name'] = doctor.doctor_email
    doc['Password'] = randomPassword
    doc['Org Identifier'] = org_identifier
    mail_dict[DETAILS] = doc
    mailer = EmailHandler(mail_dict)
    logger.info("Sending mail for doctor creation")
    mailer.send_mail()
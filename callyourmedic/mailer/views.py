from django.shortcuts import render
from cymportal.models import User, Group
from django.shortcuts import render
from django.template.loader import get_template
from mailer.tasks import *
from mailer.utils import *
# Create your views here.

import logging
import json

logger = logging.getLogger('mail')

CYM = 0
PORTAL = 1

MAIL_DEFAULT = 0
MAIL_CYM_USER = 1
MAIL_CYM_GROUP = 2
MAIL_PORTAL_USER = 3
MAIL_PORTAL_GROUP = 4
MAIL_PORTAL_PATIENT = 5
MAIL_PORTAL_DEPARTMENT = 6
MAIL_PORTAL_ORG = 7
MAIL_PORTAL_DOCTOR = 8
MAIL_ORG_CREATE = 9


def handle_mails(mail_data_dict):
    """accepts a dictionary of values of MAIL_DATA_DICT and sends mails accordingly"""

class EmailHandler:

    def __init__(self,mail_dict):
        self.mail_dict = mail_dict


    def send_mail(self):
        mail_type = self.mail_dict[TYPE]

        if mail_type == MAIL_CYM_USER:
            self.template = 'cym_user_mail.html'
            self.mail_dict[MESSAGE] = MAIL_MESSAGE_CYM_USER_CREATE
            self.mail_dict[SUBJECT] = MAIL_SUBJECT_USER_CREATE
            self.user(CYM)

        elif mail_type == MAIL_CYM_GROUP:
            self.template = 'cym_grp_mail.html'
            self.mail_dict[MESSAGE] = MAIL_MESSAGE_CYM_GROUP_CREATE
            self.mail_dict[SUBJECT] = MAIL_SUBJECT_GROUP_CREATE
            self.group(CYM)

        elif mail_type == MAIL_PORTAL_USER :
            self.template = 'portal_usr_mail.html'
            self.mail_dict[MESSAGE] = MAIL_MESSAGE_PORTAL_USER_CREATE
            self.mail_dict[SUBJECT] = MAIL_SUBJECT_USER_CREATE
            self.user(PORTAL)

        elif mail_type == MAIL_PORTAL_GROUP :
            self.template = 'portal_group_mail.html'
            self.mail_dict[MESSAGE] = MAIL_MESSAGE_PORTAL_GROUP_CREATE
            self.mail_dict[SUBJECT] = MAIL_SUBJECT_GROUP_CREATE
            self.group(PORTAL)

        elif mail_type == MAIL_ORG_CREATE:
            self.template = 'org_create_mail.html'
            self.mail_dict[MESSAGE] = MAIL_MESSAGE_ORG_CREATE
            self.mail_dict[SUBJECT] = MAIL_SUBJECT_ORG_CREATE
            self.org(PORTAL)

        elif mail_type == MAIL_PORTAL_DOCTOR:
            self.template = 'doctor_create_mail.html'
            self.mail_dict[MESSAGE] = MAIL_MESSAGE_DOCTOR_CREATE
            self.mail_dict[SUBJECT] = MAIL_SUBJECT_USER_CREATE
            self.doctor(PORTAL)

        elif mail_type == MAIL_PORTAL_PATIENT:
            self.template = 'patient_create_mail.html'
            self.mail_dict[MESSAGE] = MAIL_MESSAGE_PATIENT_CREATE
            self.mail_dict[SUBJECT] = MAIL_SUBJECT_PATIENT_CREATE
            self.patient(PORTAL)

    def user(self,type):
        if type == CYM:
            json_string = json.dumps(self.mail_dict)
            logger.info("Mailer for CYM User " + json_string)
            mail_to_send.delay(self.mail_dict[TO],self.mail_dict[FROM],self.mail_dict[CC],self.mail_dict[BCC],self.mail_dict[SUBJECT],self.mail_dict[MESSAGE],self.template,self.mail_dict[DETAILS])
        elif type == PORTAL:
            json_string = json.dumps(self.mail_dict)
            logger.info("Mailer for Portal User " + json_string)
            mail_to_send.delay(self.mail_dict[TO],self.mail_dict[FROM],self.mail_dict[CC],self.mail_dict[BCC],self.mail_dict[SUBJECT],self.mail_dict[MESSAGE],self.template,self.mail_dict[DETAILS])
        else:
            return None


    def group(self,type):
        if type == CYM:
            json_string = json.dumps(self.mail_dict)
            logger.info("Mailer for CYM Group " + json_string)
            mail_to_send.delay(self.mail_dict[TO],self.mail_dict[FROM],self.mail_dict[CC],self.mail_dict[BCC],self.mail_dict[SUBJECT],self.mail_dict[MESSAGE],self.template,self.mail_dict[DETAILS])
        elif type == PORTAL:
            json_string = json.dumps(self.mail_dict)
            logger.info("Mailer for Portal Group " + json_string)
            mail_to_send.delay(self.mail_dict[TO],self.mail_dict[FROM],self.mail_dict[CC],self.mail_dict[BCC],self.mail_dict[SUBJECT],self.mail_dict[MESSAGE],self.template,self.mail_dict[DETAILS])

    def org(self,type):
        if type == CYM:
            return
        elif type == PORTAL:
            json_string = json.dumps(self.mail_dict)
            logger.info("Mail for org creation with details : "+json_string)
            mail_to_send.delay(self.mail_dict[TO],self.mail_dict[FROM],self.mail_dict[CC],self.mail_dict[BCC],self.mail_dict[SUBJECT],self.mail_dict[MESSAGE],self.template,self.mail_dict[DETAILS])

        else:
            return

    def doctor(self,type):
        if type == CYM :
            return
        elif type == PORTAL:
            json_string = json.dumps(self.mail_dict)
            logger.info("Mail for doctor creation with details : "+json_string)
            mail_to_send.delay(self.mail_dict[TO],self.mail_dict[FROM],self.mail_dict[CC],self.mail_dict[BCC],self.mail_dict[SUBJECT],self.mail_dict[MESSAGE],self.template,self.mail_dict[DETAILS])



    def patient(self,type):
        if type == CYM:
            return
        elif type == PORTAL:
            json_string = json.dumps(self.mail_dict)
            logger.info("Mail for patient creation with details : "+json_string)
            mail_to_send.delay(self.mail_dict[TO],self.mail_dict[FROM],self.mail_dict[CC],self.mail_dict[BCC],self.mail_dict[SUBJECT],self.mail_dict[MESSAGE],self.template,self.mail_dict[DETAILS])
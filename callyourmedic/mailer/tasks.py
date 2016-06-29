from __future__ import absolute_import
from celery import shared_task


from django.core.mail import send_mail

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import traceback
import logging
import json

logger = logging.getLogger('tasks')

TYPE = "mail_type"
TO = "to"
CC = "cc"
BCC = "bcc"
FROM = "from"
MESSAGE = "message"
SUBJECT = "subject"
DETAILS = "details" # A dictionary

MAIL_DATA_DICT = {
    TYPE : None,
    TO : [],
    CC : [],
    BCC : [],
    FROM : None,
    SUBJECT : None,
    MESSAGE : None,
    DETAILS : {},
}

def mail_to_user(self,email,password,group,firstname):
    args = {}
    args['email'] = email
    args['password'] = password
    args['group'] = group
    args['username'] = firstname
    from_email = 'support@callyourmedic.com'
    to_email = [email]
    html_content = render_to_string('user_details_mail.html', args)
    text_content = strip_tags(html_content)
    subject = 'Credentials for CYM portal'
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except:
        traceback.print_exc()


@shared_task
def mail_to_send(to,from_mail,cc,bcc,subject,message,template,details):
    """GENERIC METHOD WHICH SENDS MAIL"""

    if to is None or len(to) == 0:
        return
    if from_mail is None:
        from_mail = 'support@callyourmedic.com'
    args = {}
    args["message"] = message
    args["details"] = details
    html_content = render_to_string(template,args)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_mail, to, bcc = bcc, cc = cc)
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
        emails = ''
        for mail in to:
            emails = emails + ' ' + mail
        if cc:
            for mail in cc:
                emails = emails + ' ' + mail
        if bcc:
            for mail in bcc:
                emails = emails + ' ' + mail
        logger.info("Mail sent to "+ emails)
    except:
        logger.error("Error in sending mail. Printing traceback")
        traceback.print_exc()

@shared_task
def mail_test(to,from_mail,cc,bcc,subject,message,details):
    """GENERIC METHOD WHICH SENDS MAIL"""
    if to is None or len(to) == 0:
        return
    if from_mail is None:
        from_mail = 'support@callyourmedic.com'
    args = {}
    args["message"] = message
    args["details"] = details
    html_content = render_to_string("cym_user_mail.html",args)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(subject, text_content, from_mail, to, bcc = bcc, cc = cc)
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except:
        traceback.print_exc()
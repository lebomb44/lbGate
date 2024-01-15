#! /usr/bin/env python3
# coding: utf-8


""" LbEmail"""


import smtplib
from email.mime.text import MIMEText
import urllib.parse

import settings
import fct
import myconfig


def sendto(email, subject, body):
    try:
        subject = urllib.parse.unquote_plus(subject)
        body = urllib.parse.unquote_plus(body)
        msg = MIMEText(body)
        msg["Subject"] = str(subject)
        msg["From"] = 'Jeedom ' + settings.HOSTNAME + ' <' + myconfig.EMAIL_LOGIN + '>'
        msg["To"] = ", ".join(email)
        mail = smtplib.SMTP(myconfig.EMAIL_SMTP, 587, timeout=5.0)
        mail.ehlo()
        mail.starttls()
        mail.login(myconfig.EMAIL_LOGIN, myconfig.EMAIL_PASSWORD)
        mail.sendmail(myconfig.EMAIL_LOGIN, email, msg.as_string())
        mail.close()
    except Exception as ex:
        fct.log_exception(ex)


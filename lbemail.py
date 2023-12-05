#! /usr/bin/env python3
# coding: utf-8


""" LbEmail"""


import smtplib
import urllib.parse

import settings
import fct
import myconfig


def sendto(email, object, msg):
    try:
        object = urllib.parse.unquote_plus(object)
        content = urllib.parse.unquote_plus(msg)
        mail = smtplib.SMTP(myconfig.EMAIL_SMTP, 587, timeout=5.0)
        mail.ehlo()
        mail.starttls()
        sender = myconfig.EMAIL_LOGIN
        recipient = str(email)
        recipient = recipient.replace("[","").replace("]","").replace("'","")
        mail.login(myconfig.EMAIL_LOGIN, myconfig.EMAIL_PASSWORD)
        header = 'To:' + str(recipient) + '\n' \
        + 'From:Jeedom ' + settings.HOSTNAME + ' <' + myconfig.EMAIL_LOGIN + '>\n' \
        + 'subject:' + object + '\n'
        content = header + content
        mail.sendmail(sender, recipient, content)
        mail.close()
    except Exception as ex:
        fct.log_exception(ex)


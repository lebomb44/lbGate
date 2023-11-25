#! /usr/bin/env python3
# coding: utf-8


""" LbEmail"""


import smtplib
import urllib.parse

import fct
import myconfig


def sendto(email, object, msg):
    try:
        object = urllib.parse.unquote_plus(object)
        content = urllib.parse.unquote_plus(msg)
        mail = smtplib.SMTP(myconfig.EMAIL_SMTP, 587)
        mail.ehlo()
        mail.starttls()
        sender = myconfig.EMAIL_LOGIN
        recipient = email
        mail.login(myconfig.EMAIL_LOGIN, myconfig.EMAIL_PASSWORD)
        header = 'To:' + recipient + '\n' \
        + 'From:' + myconfig.EMAIL_SENDER + '\n' \
        + 'subject:' + object + '\n'
        content = header + content
        mail.sendmail(sender, recipient, content)
        mail.close()
    except Exception as ex:
        fct.log_exception(ex)

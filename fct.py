#! /usr/bin/env python3
# coding: utf-8


""" LbGate basic functions """


from __future__ import print_function
import time
from six.moves import urllib
import requests

import settings


def log(msg):
    """ Print message with a time header """
    print(time.strftime('%Y/%m/%d %H:%M:%S: ') + msg)


def http_request(url):
    """ Do HTTP request to the URL """
    try:
        log("URL call: " + url)
        requests.get(url, timeout=0.1)
    except requests.exceptions.RequestException as ex:
        log("ERROR http_request: " + str(ex))


def send_sms(msg):
    """ Send SMS message """
    log("Send SMS: " + msg)
    http_request(settings.SMS_URL + urllib.parse.quote(msg))


def send_email(msg):
    """ Send e-mail """
    log("Send EMAIL: " + msg)
    http_request(settings.EMAIL_URL + urllib.parse.quote(msg))


def send_alert(msg):
    """ Send a global alert (SMS + E-mail) """
    send_sms(msg)
    send_email(msg)


def write_serial(node_, msg):
    """ Write the serial port if already open """
    if settings.node_list[node_]['fd'].isOpen() is True:
        settings.node_list[node_]['fd'].write(("\n\n" + node_ + " " + msg + "\n").encode('utf-8'))
        # log("Write ping to node " + node)
        settings.node_list[node_]['fd'].flushOutput()


def contact_status_set_close(key):
    """ Set contact status to 'close' """
    settings.contact_status[key] = True


def log_contact_status_set_close(key):
    """ Set contact status to 'close' and print log message """
    log("LOG contact setClose: " + key)
    contact_status_set_close(key)


def contact_status_set_open(key):
    """ Set contact status to 'open' """
    settings.contact_status[key] = False


def log_contact_status_set_open(key):
    """ Set contact status to 'open' and print log message """
    log("LOG contact setOpen: " + key)
    contact_status_set_open(key)


def move_status_set_stated(key):
    """ Set move status to 'moving' """
    settings.move_status[key] = True
    # log("Move " + key + " is at " + str(settings.move_status[key]))


def move_status_set_moving(key):
    """ Set move status to 'not moving' """
    settings.move_status[key] = False
    # log("Move " + key + " is at " + str(settings.move_status[key]))


def timeout_check(node_):
    """ Check timeout to increment """
    if settings.MAX_NODE_ERRORS > settings.node_list[node_]['errorCnt']:
        settings.node_list[node_]['errorCnt'] += 1
    if settings.MAX_NODE_ERRORS == settings.node_list[node_]['errorCnt']:
        send_alert("Timeout on serial node " + node_)
        settings.node_list[node_]['errorCnt'] += 1
    #log("=== Checked " + node_ + " timeout = " + str(settings.node_list[node_]['errorCnt']))


def timeout_reset(node_, value):
    """ Reset timeout to zero """
    #log("### Reset of " + node_ + " timeout")
    settings.node_list[node_]['errorCnt'] = 0

def temp_set(key, value):
    """ Set temperature """
    settings.temp[key] = value


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
        requests.get(url, timeout=1.0)
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
    try:
        if settings.node_list[node_]['fd'].isOpen() is True:
            settings.node_list[node_]['fd'].write((node_ + " " + msg + "\n").encode('utf-8'))
            # log("Write serial to node " + node)
            settings.node_list[node_]['fd'].flush()
    except Exception as ex:
        log("ERROR write_serial Exception: " + str(ex))


def contact_status_set_close(key):
    """ Set contact status to 'close' """
    if key in settings.contact_status:
        settings.contact_status[key] = True
    else:
        log("ERROR contact_status_set_close: " + key + " not in settings.contact_status")

def log_contact_status_set_close(key):
    """ Set contact status to 'close' and print log message """
    log("LOG contact setClose: " + key)
    contact_status_set_close(key)


def contact_status_set_open(key):
    """ Set contact status to 'open' """
    if key in settings.contact_status:
        settings.contact_status[key] = False
    else:
        log("ERROR contact_status_set_open: " + key + " not in settings.contact_status")


def log_contact_status_set_open(key):
    """ Set contact status to 'open' and print log message """
    log("LOG contact setOpen: " + key)
    contact_status_set_open(key)


def move_status_set_stated(key):
    """ Set move status to 'moving' """
    if key in settings.move_status:
        settings.move_status[key] = True
    else:
        log("ERROR move_status_set_stated: " + key + " not in settings.move_status")
    # log("Move " + key + " is at " + str(settings.move_status[key]))


def move_status_set_moving(key):
    """ Set move status to 'not moving' """
    if key in settings.move_status:
        settings.move_status[key] = False
    else:
        log("ERROR move_status_set_moving: " + key + " not in settings.move_status")
    # log("Move " + key + " is at " + str(settings.move_status[key]))


def timeout_check(node_):
    """ Check timeout to increment """
    if settings.MAX_NODE_ERRORS > settings.node_list[node_]['errorCnt']:
        settings.node_list[node_]['errorCnt'] += 1
    if settings.MAX_NODE_ERRORS == settings.node_list[node_]['errorCnt']:
        send_alert("Timeout on serial node " + node_)
        settings.node_list[node_]['errorCnt'] += 1
        try:
            if settings.node_list[node_]['fd'].isOpen() is True:
                settings.node_list[node_]['fd'].close()
                time.sleep(1.0)
            log("Opening " + settings.node_list[node_]['fd'].port)
            # log(node_list[node_]['fd'].get_settings())
            settings.node_list[node_]['fd'].baudrate = 9600
            settings.node_list[node_]['fd'].open()
            time.sleep(1.0)
            settings.node_list[node_]['fd'].close()
            settings.node_list[node_]['fd'].baudrate = 115200
            settings.node_list[node_]['fd'].open()
            time.sleep(3.0)
            settings.node_list[node_]['fd'].reset_input_buffer()
            settings.node_list[node_]['fd'].reset_output_buffer()
            #log("=== Checked " + node_ + " timeout = " + str(settings.node_list[node_]['errorCnt']))
        except Exception as ex:
            log("ERROR timeout_check Exception: " + str(ex))


def timeout_reset(node_, value):
    """ Reset timeout to zero """
    #log("### Reset of " + node_ + " timeout")
    settings.node_list[node_]['errorCnt'] = 0

def temp_set(key, value):
    """ Set temperature """
    settings.temp[key] = value


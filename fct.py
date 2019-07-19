#! /usr/bin/env python3
# coding: utf-8


""" LbGate basic functions """


from __future__ import print_function
import time
import traceback
from six.moves import urllib
import requests

import settings


def log(msg):
    """ Print message with a time header """
    print(time.strftime('%Y/%m/%d %H:%M:%S: ') + msg)


def log_exception(ex, msg="ERROR Exception"):
    """ Print exception with a time header """
    log(msg + ": " + str(ex))
    log(traceback.format_exc())


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


def call_url_if_val_change(node_, cmd_, arg_array_):
    """ Call URL only if value change from previous state """
    if node_ in settings.acq:
        if cmd_ in settings.acq[node_]:
            if 'val' in settings.acq[node_][cmd_]:
                if 'url' in settings.acq[node_][cmd_]:
                    if len(arg_array_) == 2:
                        if arg_array_[0] == 'val':
                            arg_value = type(settings.acq[node_][cmd_]['val'])(arg_array_[1])
                            if settings.acq[node_][cmd_]['val'] != arg_value:
                                http_request(settings.acq[node_][cmd_]['url'][arg_value])
                                settings.acq[node_][cmd_]['val'] = arg_value
                        else:
                            log("ERROR: 'val' key is not in arg_array_ '" + str(arg_array_) + "'")
                    else:
                        log("ERROR: len of '" + str(arg_array_) + "' is not 1")
                else:
                    log("ERROR: 'url' key is not in acq." + node_ + "." + cmd_)
            else:
                log("ERROR: 'val' key is not in acq." + node_ + "." + cmd_)
        else:
            log("ERROR: '" + cmd_ + "' is not in acq." + node_)
    else:
        log("ERROR: '" + node_ + "' is not in acq")


def temp_set(node_, cmd_, arg_array_):
    """ Set temperature """
    #settings.temp[key] = value


def timeout_reset(node_, cmd_, arg_array_):
    """ Reset timeout to zero """
    #log("### Reset of " + node_ + " timeout")
    if settings.node_list[node_].error_cnt > settings.node_list[node_].error_cnt_max:
        settings.node_list[node_].error_cnt_max = settings.node_list[node_].error_cnt
    settings.node_list[node_].error_cnt = 0
    settings.node_list[node_].ping_rx_cnt += 1

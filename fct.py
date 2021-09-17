#! /usr/bin/env python3
# coding: utf-8


""" LbGate basic functions """


from __future__ import print_function
import time
import traceback
from six.moves import urllib
import requests

import settings
import alarm


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
    msg = msg + " " + time.strftime('%Y/%m/%d %H:%M:%S')
    log("Send SMS: " + msg)
    http_request(settings.SMS_URL1 + urllib.parse.quote(msg))
    http_request(settings.SMS_URL2 + urllib.parse.quote(msg))


def send_email(msg):
    """ Send e-mail """
    msg = msg + " " + time.strftime('%Y/%m/%d %H:%M:%S')
    log("Send EMAIL: " + msg)
    http_request(settings.EMAIL_URL1 + urllib.parse.quote(msg))
    http_request(settings.EMAIL_URL2 + urllib.parse.quote(msg))


def send_alert(msg):
    """ Send a global alert (SMS + E-mail) """
    send_sms(msg)
    send_email(msg)


def call_rts_if_val_change(node_, cmd_, arg_array_):
    """ Call RTS command only if value change from previous state """
    #if node_ == "kitchen":
    #    log("DEBUG call_rts_if_val_change: node=" + node_ + ", cmd=" + cmd_ + ", arg=" + str(arg_array_))
    if node_ in settings.acq:
        if cmd_ in settings.acq[node_]:
            if 'val' in settings.acq[node_][cmd_]:
                if 'rts' in settings.acq[node_][cmd_]:
                    if len(arg_array_) == 2:
                        if arg_array_[0] == 'val':
                            arg_value = type(settings.acq[node_][cmd_]['val'])(arg_array_[1])
                            if settings.acq[node_][cmd_]['val'] != arg_value:
                                settings.rts.write(settings.acq[node_][cmd_]['rts'][arg_value])
                                settings.acq[node_][cmd_]['val'] = arg_value
                        else:
                            log("ERROR: 'val' key is not in arg_array_ '" + str(arg_array_) + "'")
                    else:
                        log("ERROR: len of '" + str(arg_array_) + "' is not 1")
                else:
                    log("ERROR: 'rts' key is not in acq." + node_ + "." + cmd_)
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


def nfcTag(node_, cmd_, arg_array_):
    """ NFC Tag detected """
    log("WARNING nfcTag: node=" + node_ + ", cmd=" + cmd_ + ", arg=" + str(arg_array_))
    if node_ == 'entry' and cmd_ == 'nfcTag' and len(arg_array_) == 3:
        authorized = ['Olivier_Cambon', 'Stephanie_Cambon', 'Ellis_Cambon', 'Key1_Cambon', 'Key2_Cambon']
        fullname = str(arg_array_[1]) + "_" + str(arg_array_[2])
        if arg_array_[0] == 'get' and fullname in authorized:
            if settings.alarm['is_enabled'] is False:
                if alarm.enable() is True:
                    http_request(settings.ALARM_NAME_URL + fullname)
            else:
                alarm.disable()
                http_request(settings.ALARM_NAME_URL + fullname)

#! /usr/bin/env python3
# coding: utf-8


""" LbSms"""


import io
import threading
import time
import datetime
import fcntl
import os
import queue
import urllib.parse

import fct


class Sms(threading.Thread):
    """ Class for a serial port """
    def __init__(self, name):
        self.dict = dict()
        self.dict["port"] = "/dev/" + name
        self.dict["node_name"] = name
        self.dict["ok_date"] = "Unknown"
        self.dict["signal_quality"] = 0
        self.dict["signal_quality_date"] = "Unknown"
        self.dict["open_cnt"] = 0
        self.dict["nb_config"] = 0
        self.dict["nb_loop"] = 0
        self.dict["is_loop_enabled"] = True
        self.dict["cmd_tx_cnt"] = 0
        self.dict["cmd_rx_cnt"] = 0
        self.dict["cmd_rx_ok_cnt"] = 0
        self.dict["cmd_rx_signal_quality_cnt"] = 0
        self.fd_port = io.IOBase()
        self.line = ""
        self.smsqueue = queue.Queue(1000)
        self.read_iter = 0
        threading.Thread.__init__(self, name=name)


    def run(self):
        """ Cyclic execution to poll for received characters """
        self.dict["nb_loop"] = 1
        while self.dict["is_loop_enabled"] is True:
            try:
                #fct.log("DEBUG: " + self.dict["node_name"] + " loop " + str(loop_nb))
                if self.is_open() is False:
                    self.open()
                    time.sleep(1.0)
                if self.is_open() is True:
                    line = ""
                    cserial = " "
                    read_iter_ = 0
                    while (len(cserial) > 0) and (self.dict["is_loop_enabled"] is True):
                        try:
                            cserial = self.fd_port.read(1)
                            if cserial is None:
                                cserial = ""
                            else:
                                cserial = cserial.decode(encoding='utf-8', errors='ignore')
                            if len(cserial) > 0:
                                read_iter_ = read_iter_ + 1
                                if ord(cserial) == 0:
                                    cserial = ""
                            else:
                                cserial = ""
                            if (self.line != "") and (cserial == "\n" or cserial == "\r"):
                                line = self.line
                                self.line = ""
                                # fct.log("DEBUG New line create=" + line)
                                break
                            else:
                                if (cserial != "\n") and (cserial != "\r"):
                                    self.line = self.line + cserial
                        except Exception as ex:
                            self.line = ""
                            cserial = ""
                            fct.log_exception(ex, msg="ERROR while decoding data on " + self.dict["node_name"])
                            self.close()
                    if read_iter_ > self.read_iter:
                        self.read_iter = read_iter_
                    if line != "":
                        self.dict["cmd_rx_cnt"] += 1
                        #fct.log("DEBUG: line=" + str(line))
                        if "OK" in line:
                            self.dict["cmd_rx_ok_cnt"] += 1
                            self.dict["ok_date"] = str(datetime.datetime.now())
                        else:
                            line_array = line.split(" ")
                            #fct.log("DEBUG: line_array=" + str(line_array))
                            if len(line_array) == 2:
                                if line_array[0] == "+CSQ:":
                                    try:
                                        self.dict["signal_quality"] = int(round(float(line_array[1].replace(",","."))))
                                        self.dict["cmd_rx_signal_quality_cnt"] += 1
                                        self.dict["signal_quality_date"] = str(datetime.datetime.now())
                                    except Exception as ex:
                                        self.dict["signal_quality"] = 0
                                        fct.log_exception(ex)
                        line = ""
                    if self.dict["nb_loop"] % 50000 == 0:
                        self.config()
                    if self.dict["nb_loop"] % 1000 == 0:
                        if self.smsqueue.empty() is False:
                            try:
                                msg = self.smsqueue.get()
                                if msg != '':
                                    self.write(msg)
                            except Exception as ex:
                                fct.log_exception(ex)
                else:
                    self.dict["signal_quality"] = 0
            except Exception as ex:
                fct.log_exception(ex)
                self.close()
            self.dict["nb_loop"] += 1
            if self.dict["nb_loop"] >= 1000000:
                self.dict["nb_loop"] = 0
            time.sleep(0.001)


    def stop(self):
        """ Stop polling loop """
        fct.log("Stopping " + self.dict["node_name"] + " thread...")
        self.dict["is_loop_enabled"] = False
        time.sleep(1.0)
        fct.log("Closing " + self.dict["node_name"] + " node...")
        if self.is_open() is True:
            self.fd_port.close()


    def is_open(self):
        """ Check if serial port is already open """
        try:
            ret = fcntl.fcntl(self.fd_port, fcntl.F_GETFD)
            return ret >= 0
        except:
            return False


    def open(self):
        """ Open the serial port """
        try:
            fct.log("Opening " + self.dict["node_name"])
            self.fd_port = open(self.dict["port"], "rb+", buffering=0)
            fd_port = self.fd_port.fileno()
            flag = fcntl.fcntl(fd_port, fcntl.F_GETFL)
            fcntl.fcntl(fd_port, fcntl.F_SETFL, flag | os.O_NONBLOCK | os.O_NOCTTY)
            self.dict["open_cnt"] += 1
            self.dict["nb_config"] = 0
            self.dict["ok_date"] = "Unknown"
            self.dict["signal_quality"] = 0
            self.dict["signal_quality_date"] = "Unknown"
            self.dict["cmd_tx_cnt"] = 0
            self.dict["cmd_rx_cnt"] = 0
            self.dict["cmd_rx_ok_cnt"] = 0
            self.dict["cmd_rx_signal_quality_cnt"] = 0
        except Exception as ex:
            fct.log_exception(ex)


    def close(self):
        """ Close the serial port """
        try:
            if self.is_open() is True:
                fct.log("Closing " + self.dict["node_name"])
                self.fd_port.close()
            self.dict["signal_quality"] = 0
        except Exception as ex:
            fct.log_exception(ex)


    def write(self, msg):
        """ Write the serial port if already open """
        try:
            if self.is_open() is True:
                self.fd_port.write((msg + "\r").encode('utf-8'))
                #fct.log("DEBUG: Write serial to node " + self.dict["node_name"] + ": " + msg)
                self.fd_port.flush()
                self.dict["cmd_tx_cnt"] += 1
        except Exception as ex:
            fct.log_exception(ex)
            self.close()


    def config(self):
        """ Configure modem """
        try:
            self.smsqueue.put_nowait('ATZ')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('AT+CMGF=1')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('AT+CSCA="+33695000695"')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('AT+CSQ')
            self.smsqueue.put_nowait('')
            self.dict["nb_config"] += 1
        except Exception as ex:
            fct.log_exception(ex)


    def sendto(self, phone, msg):
        """ Send SMS message to phone number """
        try:
            msg = urllib.parse.unquote_plus(msg)
            self.smsqueue.put_nowait('AT+CMGS="' + str(phone) + '"')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait(str(msg) + "\x1A")
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('')
        except Exception as ex:
            fct.log_exception(ex)


    def callto(self, phone):
        """ Send SMS message to phone number """
        try:
            self.smsqueue.put_nowait('ATD' + str(phone) + ';')
            for i in range(0,30):
                self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('ATH')
            self.smsqueue.put_nowait('')
            self.smsqueue.put_nowait('')
        except Exception as ex:
            fct.log_exception(ex)


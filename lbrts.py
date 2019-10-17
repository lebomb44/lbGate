#! /usr/bin/env python3
# coding: utf-8


""" LbRts"""


import io
import threading
import time
import fcntl
import os
import json

import fct
import settings


class Rts(threading.Thread):
    """ Class for a serial port """
    def __init__(self, name):
        self.port = "/dev/" + name
        self.node_name = name
        self.fd_port = io.IOBase()
        self.line = ""
        self.open_cnt = 0
        self.read_iter = 0
        self.is_loop_enabled = True
        threading.Thread.__init__(self, name=name)


    def run(self):
        """ Cyclic execution to poll for received characters """
        loop_nb = 1
        while self.is_loop_enabled is True:
            try:
                #fct.log("DEBUG: " + self.node_name + " loop " + str(loop_nb))
                if self.is_open() is False:
                    self.open()
                    time.sleep(1.0)
                if self.is_open() is True:
                    line = ""
                    cserial = " "
                    read_iter_ = 0
                    while (len(cserial) > 0) and (self.is_loop_enabled is True):
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
                            fct.log_exception(ex, msg="ERROR while decoding data on " + self.node_name)
                            self.close()
                    if read_iter_ > self.read_iter:
                        self.read_iter = read_iter_
                    if line != "":
                        if line.startswith("ZIA33"):
                            try:
                                resp = json.loads(line[5:])
                                #fct.log("DEBUG: line_array=" + str(json.dumps(resp)))
                                if resp["frame"]["header"]["protocolMeaning"] == "CHACON":
                                    if resp["frame"]["infos"]["id"] == "1060074882":
                                        if resp["frame"]["infos"]["subTypeMeaning"] == "ON":
                                            #fct.log("DEBUG: CHACON cmd ON")
                                            fct.http_request('http://localhost:' + str(settings.HTTPD_PORT) + '/api/ext/waterMainRelay/set/1')
                                            fct.http_request('http://localhost:' + str(settings.HTTPD_PORT) + '/api/ext/waterGardenRelay/set/1')
                                        elif resp["frame"]["infos"]["subTypeMeaning"] == "OFF":
                                            #fct.log("DEBUG: CHACON cmd OFF")
                                            fct.http_request('http://localhost:' + str(settings.HTTPD_PORT) + '/api/ext/waterMainRelay/set/0')
                                            fct.http_request('http://localhost:' + str(settings.HTTPD_PORT) + '/api/ext/waterGardenRelay/set/0')
                                        else:
                                            fct.log("WARNING: CHACON type unknown")
                                    else:
                                        fct.log("WARNING: CHACON id unknown")
                                else:
                                    fct.log("WARNING: RfPlayer protocol unknown")
                            except Exception as ex:
                                fct.log_exception(ex)
                        else:
                            fct.log("WARNING: RfPlayer line does not start with 'ZIA33': " + str(line))
            except Exception as ex:
                fct.log_exception(ex)
                self.close()
            loop_nb += 1
            time.sleep(0.001)


    def stop(self):
        """ Stop polling loop """
        fct.log("Stopping " + self.node_name + " thread...")
        self.is_loop_enabled = False
        time.sleep(1.0)
        fct.log("Closing " + self.node_name + " node...")
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
            fct.log("Opening " + self.node_name)
            self.fd_port = open(self.port, "rb+", buffering=0)
            fd_port = self.fd_port.fileno()
            flag = fcntl.fcntl(fd_port, fcntl.F_GETFL)
            fcntl.fcntl(fd_port, fcntl.F_SETFL, flag | os.O_NONBLOCK)
            self.write("HELLO")
            self.write("FORMAT OFF")
            self.write("STATUS JSON")
            self.write("FORMAT JSON")
        except Exception as ex:
            fct.log_exception(ex)


    def close(self):
        """ Close the serial port """
        try:
            if self.is_open() is True:
                fct.log("Closing " + self.node_name)
                self.fd_port.close()
        except Exception as ex:
            fct.log_exception(ex)


    def write(self, msg):
        """ Write the serial port if already open """
        try:
            if self.is_open() is True:
                self.fd_port.write(("ZIA++" + msg + "\r\r").encode('utf-8'))
                self.fd_port.write(("ZIA++" + msg + "\r\r").encode('utf-8'))
                fct.log("Write serial to node " + self.node_name + ": " + msg)
                self.fd_port.flush()
        except Exception as ex:
            fct.log("ERROR write_serial Exception: " + str(ex))


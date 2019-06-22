#! /usr/bin/env python3
# coding: utf-8


""" LbSerial"""


import io
import threading
import time
import fcntl
import os

import fct
import settings


class Serial(threading.Thread):
    def __init__(self, name):
        self.port = "/dev/" + name
        self.nodeName = name
        self.fd = io.IOBase()
        self.errorCnt = 0
        self.errorCntMax = 0
        self.cmdRxCnt = 0
        self.pingTxCnt = 0
        self.pingRxCnt = 0
        self.line = ""
        self.openCnt = 0
        self.readIter = 0
        self.is_loop_enabled = True
        threading.Thread.__init__(self, name=name)

    def run(self):
        loop_nb = 1
        while self.is_loop_enabled is True:
            try:
                #fct.log("DEBUG: " + self.nodeName + " loop " + str(loop_nb))
                if self.isOpen() is False:
                    self.open()
                    time.sleep(1.0)
                if self.isOpen() is True:
                    line = ""
                    cserial = " "
                    readIter_ = 0
                    while (len(cserial) > 0) and (self.is_loop_enabled is True):
                        try:
                            cserial = self.fd.read(1)
                            if cserial is None:
                                cserial = ""
                            else:
                                cserial = cserial.decode(encoding='utf-8', errors='ignore')
                            if len(cserial) > 0:
                                readIter_ = readIter_ + 1
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
                            fct.logException(ex, msg="ERROR while decoding data on " + self.nodeName)
                            self.close()
                    if readIter_ > self.readIter:
                        self.readIter = readIter_
                    if line != "":
                        line_array = line.split(" ")
                        # fct.log("DEBUG: line_array=" + str(line_array))
                        if len(line_array) > 2:
                            node = line_array[0]
                            cmd = line_array[1]
                            if node in settings.acq:
                                if cmd in settings.acq[node]:
                                    arg_map = line_array[2:]
                                    if 'fct' in settings.acq[node][cmd]:
                                        try:
                                            settings.acq[node][cmd]['fct'](node, cmd, arg_map)
                                        except Exception as ex:
                                            fct.logException(ex)
                                    else:
                                        if len(arg_map) == 2:
                                            if arg_map[0] in settings.acq[node][cmd]:
                                                settings.acq[node][cmd][arg_map[0]] = type(settings.acq[node][cmd][arg_map[0]])(arg_map[1])
                                            else:
                                                fct.log("ERROR: " + arg_map[0] + " is not in cmd " + node + "." + cmd)
                                        else:
                                            if len(arg_map) == 3:
                                                if arg_map[0] in settings.acq[node][cmd]:
                                                    if arg_map[1] in settings.acq[node][cmd][arg_map[0]]:
                                                        settings.acq[node][cmd][arg_map[0]][arg_map[1]] = type(settings.acq[node][cmd][arg_map[0]][arg_map[1]])(arg_map[2])
                                                    else:
                                                        fct.log("ERROR: " + arg_map[1] + " is not in cmd " + node + "." + cmd + "." + arg_map[0])
                                                else:
                                                    fct.log("ERROR: " + arg_map[0] + " is not in cmd " + node + "." + cmd)
                                            else:
                                                fct.log("ERROR: incorrect number of arguments in '" + str(arg_map) + "'. Got " + str(len(arg_map)) + ", expected 2")
                                    self.cmdRxCnt += 1
                                else:
                                    fct.log("ERROR: " + cmd + " is not in node " + node)
                            else:
                                fct.log("ERROR: node '" + node + "' is unknown")
                        else:
                            fct.log("ERROR: line '" + line + "' is too short")
                    if loop_nb % 500 == 0:
                        self.write("ping get")
                        # fct.log("DEBUG PING to node " + node)
                        self.pingTxCnt += 1
            except Exception as ex:
                fct.logException(ex)
                self.close()
            self.timeout_check()
            loop_nb += 1
            if loop_nb >= 1000000:
                loop_nb = 0
            time.sleep(0.001)


    def stop(self):
        fct.log("Stopping " + self.nodeName + " thread...")
        self.is_loop_enabled = False
        time.sleep(1.0)
        fct.log("Closing " + self.nodeName + " node...")
        if self.isOpen() is True:
            self.fd.close()

    def isOpen(self):
        try:
            ret = fcntl.fcntl(self.fd, fcntl.F_GETFD)
            return (0 <= ret)
        except Exception as ex:
            return False


    def open(self):
        try:
            fct.log("Opening " + self.nodeName)
            self.fd = open(self.port, "rb+", buffering=0)
            fd = self.fd.fileno()
            flag = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, flag | os.O_NONBLOCK)
            self.openCnt += 1
        except Exception as ex:
            fct.logException(ex)


    def close(self):
        try:
            if self.isOpen() is True:
                fct.log("Closing " + self.nodeName)
                self.fd.close()
        except Exception as ex:
            fct.logException(ex)


    def write(self, msg):
        """ Write the serial port if already open """
        try:
            if self.isOpen() is True:
                self.fd.write((self.nodeName + " " + msg + "\n").encode('utf-8'))
                # fct.log("Write serial to node " + self.nodeName)
                self.fd.flush()
        except Exception as ex:
            fct.log("ERROR write_serial Exception: " + str(ex))


    def timeout_check(self):
        """ Check timeout to increment """
        if settings.MAX_NODE_ERRORS > self.errorCnt:
            self.errorCnt += 1
        if settings.MAX_NODE_ERRORS == self.errorCnt:
            fct.send_alert("Timeout on serial node " + self.nodeName)
            self.errorCnt += 1
            self.close()
            time.sleep(1.0)
            self.open()


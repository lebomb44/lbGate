#! /usr/bin/env python3
# coding: utf-8


""" LbSms"""


import io
import time
import fcntl
import os

import fct
import settings


class Sms():
    """ Class for a serial port """
    def __init__(self, name):
        self.port = "/dev/" + name
        self.node_name = name
        self.fd_port = io.IOBase()


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
                self.fd_port.write((msg + "\r\n").encode('utf-8'))
                fct.log("Write serial to node " + self.node_name + ": " + msg)
                self.fd_port.flush()
        except Exception as ex:
            fct.log("ERROR write_serial Exception: " + str(ex))


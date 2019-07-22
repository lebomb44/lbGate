#! /usr/bin/env python3
# coding: utf-8


""" Presence """


import threading
import time
import datetime
import random

import fct
import settings


class Presence(threading.Thread):
    """ Class for light presence """
    def __init__(self, name):
        self.is_loop_enabled = True
        threading.Thread.__init__(self, name=name)

    def run(self):
        """ Cyclic execution of light ON/OFF simulating presence """
        while self.is_loop_enabled is True:
            if datetime.datetime.now().hour >= 22 or datetime.datetime.now().hour <= 6:
                if settings.presence_is_enabled is True or settings.alarm_is_enabled is True:
                    settings.node_list['kitchen'].write('entryRelay set 1')
                n_sec = random.randint(10, 15)*60
                for n_loop in range(0, n_sec):
                    if settings.presence_is_enabled is True or settings.alarm_is_enabled is True:
                        time.sleep(1.0)
                if settings.presence_is_enabled is True or settings.alarm_is_enabled is True:
                    settings.node_list['kitchen'].write('entryRelay set 0')
                n_sec = random.randint(15, 30)*60
                for n_loop in range(0, n_sec):
                    if settings.presence_is_enabled is True or settings.alarm_is_enabled is True:
                        time.sleep(1.0)
            if settings.presence_is_enabled is False and settings.alarm_is_enabled is False:
                settings.node_list['kitchen'].write('entryRelay set 0')
            time.sleep(10.0)


    def stop(self):
        """ Stop polling loop """
        fct.log("Stopping presence thread...")
        self.is_loop_enabled = False
        time.sleep(1.0)

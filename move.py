#! /usr/bin/env python3
# coding: utf-8


""" Move sensor management """


import datetime

import settings
import fct


move_timeout = 0


def run():
    global move_timeout
    if settings.move_is_enabled is True:
        try:
            fct.write_serial("safety", "moveRelay set 1")
        except Exception as ex:
            fct.log("ERROR Exception: " + str(ex))
        if datetime.datetime.now().hour >= 23 or datetime.datetime.now().hour <= 6:
            for sensor in settings.move_status:
                if settings.move_status[sensor] is False:
                    if sensor == "safety moveCoridorContact":
                        fct.write_serial("bedroom", "lightRelay set 1")
                        move_timeout = 0
                    elif sensor == "safety moveDiningContact":
                        fct.write_serial("dining", "lightRelay set 1")
                        move_timeout = 0
                    elif sensor == "safety moveEntryContact":
                        fct.write_serial("kitchen", "lightRelay set 1")
                        move_timeout = 0
        if move_timeout > 20:
            fct.write_serial("bedroom", "lightRelay set 0")
            fct.write_serial("dining", "lightRelay set 0")
            fct.write_serial("kitchen", "lightRelay set 0")
        else:
            move_timeout = move_timeout + 1
    else:
        try:
            fct.write_serial("safety", "moveRelay set 0")
        except Exception as ex:
            fct.log("ERROR Exception: " + str(ex))

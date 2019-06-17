#! /usr/bin/env python3
# coding: utf-8


""" Move sensor management """


import datetime

import settings
import fct


move_timeout = 0


def run():
    global move_timeout
    try:
        if settings.move_is_enabled is True:
            try:
                settings.node_list["safety"].write("moveRelay set 1")
            except Exception as ex:
                fct.logException(ex)
            if datetime.datetime.now().hour >= 23 or datetime.datetime.now().hour <= 6:
                for nodeName, nodeValue in settings.acq.items():
                    for sensorName, sensorValue in nodeValue.items():
                        if 'type' in sensorValue:
                            if "move" in sensorValue['type']:
                                if sensorValue['val'] == 0:
                                    if sensorName == "moveCoridorContact":
                                        settings.node_list["bedroom"].write("lightRelay set 1")
                                        move_timeout = 0
                                    elif sensorName == "moveDiningContact":
                                        settings.node_list["dining"].write("lightRelay set 1")
                                        move_timeout = 0
                                    elif sensorName == "moveEntryContact":
                                        settings.node_list["kitchen"].write("lightRelay set 1")
                                        move_timeout = 0
            if move_timeout < 30:
                move_timeout = move_timeout + 1
                if move_timeout > 20:
                    settings.node_list["bedroom"].write("lightRelay set 0")
                    settings.node_list["dining"].write("lightRelay set 0")
                    settings.node_list["kitchen"].write("lightRelay set 0")
        else:
            try:
                settings.node_list["safety"].write("moveRelay set 0")
            except Exception as ex:
                fct.logException(ex)
    except Exception as ex:
        fct.logException(ex)

#! /usr/bin/env python3
# coding: utf-8


""" Move sensor management """


import datetime

import settings
import fct


move_timeout = 0


def run():
    """
        Cyclic execution to update light
    """
    global move_timeout
    try:
        if settings.move_is_enabled is True:
            try:
                settings.node_list["safety"].write("moveRelay set 1")
            except Exception as ex:
                fct.log_exception(ex)
            if datetime.datetime.now().hour >= 23 or datetime.datetime.now().hour <= 6:
                for node_name, node_value in settings.acq.items():
                    for sensor_name, sensor_value in node_value.items():
                        if 'type' in sensor_value:
                            if "move" in sensor_value['type']:
                                if sensor_value['val'] == 0:
                                    if sensor_name == "moveCoridorContact":
                                        settings.node_list["bedroom"].write("lightRelay set 1")
                                        move_timeout = 0
                                    elif sensor_name == "moveDiningContact":
                                        settings.node_list["dining"].write("lightRelay set 1")
                                        move_timeout = 0
                                    elif sensor_name == "moveEntryContact":
                                        settings.node_list["kitchen"].write("lightRelay set 1")
                                        settings.node_list["safety"].write("lightAlarm set 1")
                                        move_timeout = 0
            if move_timeout < 30:
                move_timeout = move_timeout + 1
                if move_timeout > 20:
                    settings.node_list["bedroom"].write("lightRelay set 0")
                    settings.node_list["dining"].write("lightRelay set 0")
                    settings.node_list["kitchen"].write("lightRelay set 0")
                    settings.node_list["safety"].write("lightAlarm set 0")
        else:
            try:
                settings.node_list["safety"].write("moveRelay set 0")
            except Exception as ex:
                fct.log_exception(ex)
    except Exception as ex:
        fct.log_exception(ex)

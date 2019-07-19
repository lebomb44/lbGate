#! /usr/bin/env python3
# coding: utf-8


""" Move sensor management """


import copy

import settings
import fct


def run():
    """
        Cycle execution to poll on sensors
    """
    try:
        if settings.alarm_is_enabled is True:
            if settings.alarm_triggered is True:
                if 10*60 < settings.alarm_timeout:
                    settings.node_list["safety"].write("buzzerRelay set 0")
                    if settings.alarm_stopped is False:
                        fct.send_alert("BUZZER stopped")
                        settings.alarm_stopped = True
                else:
                    settings.alarm_timeout = settings.alarm_timeout + 1
                    settings.node_list["safety"].write("buzzerRelay set 1")
            else:
                msg = ""
                for node_name, node_value in settings.acq.items():
                    for sensor_name, sensor_value in node_value.items():
                        if 'type' in sensor_value:
                            if "alarm" in sensor_value['type']:
                                #fct.log("DEBUG: checking alarm: " + node_name + "." + sensor_name + ": " + str(sensor_value['val']) + " / " + str(settings.alarm_initial_status[node_name][sensor_name]['val']))
                                if sensor_value['val'] != settings.alarm_initial_status[node_name][sensor_name]['val']:
                                    msg = msg + " " + node_name + "." + sensor_name
                                    settings.alarm_triggered = True
                            if "move" in sensor_value['type']:
                                if sensor_value['val'] == 0:
                                    msg = msg + " " + node_name + "." + sensor_name
                                    settings.alarm_triggered = True
                if settings.alarm_triggered is True:
                    settings.alarm_timeout = 0
                    settings.alarm_stopped = False
                    settings.node_list["safety"].write("buzzerRelay set 1")
                    fct.send_alert("ALARM started:" + msg)
                else:
                    settings.node_list["safety"].write("buzzerRelay set 0")
        else:
            #fct.log("DEBUG: alarm is not enabled. Copying acq to alarm_initial_status")
            settings.alarm_initial_status = copy.deepcopy(settings.acq)
            settings.node_list["safety"].write("buzzerRelay set 0")
    except Exception as ex:
        fct.log_exception(ex)

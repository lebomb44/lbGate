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
        alarm_sum = 1
        for node_name, node_value in settings.acq.items():
            for sensor_name, sensor_value in node_value.items():
                if 'type' in sensor_value:
                    if "alarm" in sensor_value['type']:
                        if sensor_value['val'] == 0:
                            alarm_sum = 0
        settings.alarm['contacts'] = alarm_sum
        if settings.alarm['is_enabled'] is True:
            if settings.alarm['triggered'] is True:
                if 10*60 < settings.alarm['timeout']:
                    settings.node_list["safety"].write("buzzerRelay set 0")
                    if settings.alarm['stopped'] is False:
                        fct.send_alert("BUZZER stopped")
                        settings.alarm['stopped'] = True
                else:
                    settings.alarm['timeout'] = settings.alarm['timeout'] + 1
                    settings.node_list["safety"].write("buzzerRelay set 1")
            else:
                msg = ""
                for node_name, node_value in settings.acq.items():
                    for sensor_name, sensor_value in node_value.items():
                        if 'type' in sensor_value:
                            if "alarm" in sensor_value['type']:
                                #fct.log("DEBUG: checking alarm: " + node_name + "." + sensor_name + ": " + str(sensor_value['val']) + " / " + str(settings.alarm['initial_status'][node_name][sensor_name]['val']))
                                if sensor_value['val'] != settings.alarm['initial_status'][node_name][sensor_name]['val']:
                                    msg = msg + " " + node_name + "." + sensor_name
                                    settings.alarm['triggered'] = True
                            if "move" in sensor_value['type']:
                                if sensor_value['val'] == 0:
                                    msg = msg + " " + node_name + "." + sensor_name
                                    settings.alarm['triggered'] = True
                if settings.alarm['triggered'] is True:
                    settings.alarm['timeout'] = 0
                    settings.alarm['stopped'] = False
                    settings.node_list["safety"].write("buzzerRelay set 1")
                    fct.send_alert("ALARM started:" + msg)
                else:
                    settings.node_list["safety"].write("buzzerRelay set 0")
        else:
            #fct.log("DEBUG: alarm is not enabled. Copying acq to alarm.initial_status")
            settings.alarm['initial_status'] = copy.deepcopy(settings.acq)
            settings.node_list["safety"].write("buzzerRelay set 0")
    except Exception as ex:
        fct.log_exception(ex)

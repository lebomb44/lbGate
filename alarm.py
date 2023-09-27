#! /usr/bin/env python3
# coding: utf-8


""" Move sensor management """


import copy
import time

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
                    # Turn on the buzzer
                    settings.node_list["safety"].write("buzzerRelay set 1")
                    # Close all the shutters
                    settings.rts.write("OFF ID 22 RTS")
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
                            if settings.alarm['use_move'] is True:
                                if "move" in sensor_value['type']:
                                    if sensor_value['val'] == 0:
                                        msg = msg + " " + node_name + "." + sensor_name
                                        settings.alarm['triggered'] = True
                if settings.alarm['triggered'] is True:
                    settings.alarm['timeout'] = 0
                    settings.alarm['stopped'] = False
                    settings.node_list["safety"].write("buzzerRelay set 1")
                    fct.send_alert("ALARM started:" + msg)
                    # Turn ON the music
                    # requests.post("http://osmc:8080/jsonrpc?Player.Stop", '{"jsonrpc":"2.0","method":"Player.Stop","params":[0],"id":1}')
                    # requests.post("http://osmc:8080/jsonrpc?Player.Open", '{"jsonrpc":"2.0","method":"Player.Open","params":{"item":{"file":"/home/osmc/alarm.mp3"},"options":{"repeat":"all"}},"id":2}')
                else:
                    settings.node_list["safety"].write("buzzerRelay set 0")
        else:
            #fct.log("DEBUG: alarm is not enabled. Copying acq to alarm.initial_status")
            settings.alarm['initial_status'] = copy.deepcopy(settings.acq)
            settings.node_list["safety"].write("buzzerRelay set 0")
    except Exception as ex:
        fct.log_exception(ex)


def enable():
    msg = ""
    timeout_ = 0
    trigger_ = True
    settings.node_list["entry"].write("lightMode set 1")
    while (timeout_ < 10) and (trigger_ is True):
        trigger_ = False
        msg = ""
        for node_name, node_value in settings.acq.items():
            for sensor_name, sensor_value in node_value.items():
                if 'type' in sensor_value:
                    if "move" in sensor_value['type']:
                        if sensor_value['val'] == 0:
                            msg = msg + " " + node_name + "." + sensor_name
                            trigger_ = True
        if trigger_ is False:
            break
        time.sleep(1)
        timeout_ += 1
    if trigger_ is False:
        settings.alarm['is_enabled'] = True
        settings.alarm['triggered'] = False
        settings.alarm['timeout'] = 0
        settings.alarm['stopped'] = False
        perimeter_is_open_ = False
        for node_name, node_value in settings.acq.items():
            for sensor_name, sensor_value in node_value.items():
                if 'type' in sensor_value:
                    if "alarm" in sensor_value['type']:
                        if sensor_value['val'] == 0:
                            perimeter_is_open_ = True
        if perimeter_is_open_ is False:
            settings.node_list["entry"].write("lightMode set 2")
        return True
    else:
        fct.send_alert("ERROR : Alarm NOT enabled : " + msg)
        settings.node_list["entry"].write("lightMode set 0")
        return False


def disable():
    settings.alarm['is_enabled'] = False
    settings.alarm['triggered'] = False
    settings.alarm['timeout'] = 0
    settings.alarm['stopped'] = False
    settings.node_list["entry"].write("lightMode set 0")

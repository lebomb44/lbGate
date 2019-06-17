#! /usr/bin/env python3
# coding: utf-8


""" Move sensor management """


import settings
import fct


def run():
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
                for nodeName, nodeValue in settings.acq.items():
                    for sensorName, sensorValue in nodeValue.items():
                        if 'type' in sensorValue:
                            if "alarm" in sensorValue['type']:
                                if sensorValue['val'] != settings.alarm_initial_status[nodeName][sensorName]['val']:
                                    msg = msg + " " + nodeName + "." + sensorName
                                    settings.alarm_triggered = True
                            if "move" in sensorValue['type']:
                                if sensorValue['val'] == 0:
                                    msg = msg + " " + nodeName + "." + sensorName
                                    settings.alarm_triggered = True
                if settings.alarm_triggered is True:
                    settings.alarm_timeout = 0
                    settings.alarm_stopped = False
                    settings.node_list["safety"].write("buzzerRelay set 1")
                    fct.send_alert("ALARM started:" + msg)
        else:
            settings.alarm_initial_status = settings.acq.copy()
    except Exception as ex:
        fct.logException(ex)

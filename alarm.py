#! /usr/bin/env python3
# coding: utf-8


""" Move sensor management """


import settings
import fct


def run():
    if settings.alarm_is_enabled is True:
        if settings.alarm_triggered is True:
            if 10*60 < settings.alarm_timeout:
                settings.alarm_triggered = False
                fct.write_serial("safety", "buzzerRelay set 0")
                fct.send_alert("ALARM stopped")
            else:
                settings.alarm_timeout = settings.alarm_timeout + 1
                fct.write_serial("safety", "buzzerRelay set 1")
        else:
            if settings.contact_status != settings.alarm_initial_status:
                msg = ""
                for sensor in settings.contact_status:
                    if settings.contact_status[sensor] != settings.alarm_initial_status[sensor]:
                        msg += sensor + "=" + settings.contact_status[sensor] + ", "
                settings.alarm_triggered = True
                settings.alarm_timeout = 0
                fct.write_serial("safety", "buzzerRelay set 1")
                fct.send_alert("ALARM contact started: " + msg)
            elif settings.move_is_enabled is True:
                for sensor in settings.move_status:
                    if settings.move_status[sensor] is False:
                        settings.alarm_triggered = True
                        settings.alarm_timeout = 0
                        fct.write_serial("safety", "buzzerRelay set 1")
                        fct.send_alert("ALARM move started: " + sensor)
    else:
        settings.alarm_initial_status = settings.contact_status.copy()

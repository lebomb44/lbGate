#! /usr/bin/env python3
# coding: utf-8


""" LbGate settings, global variables"""


import time
import copy

import fct
import lbserial


HTTPD_PORT = 8444
MAX_NODE_ERRORS = 10000
SMS_URL = ('http://localhost/core/api/jeeApi.php?'
           'apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&'
           'type=cmd&id=288&title=Jeedom&message=')
EMAIL_URL = ('http://localhost/core/api/jeeApi.php?'
             'apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&'
             'type=cmd&id=225&title=Jeedom&message=')


node_list = dict(
    bedroom=lbserial.Serial('bedroom'),
    safety=lbserial.Serial('safety'),
    dining=lbserial.Serial('dining'),
    kitchen=lbserial.Serial('kitchen'),
    ext=lbserial.Serial('ext'))

acq = dict({
    'ext': {
        'ping': {'val': 0, 'fct': fct.timeout_reset},
        'waterMainRelay': {'val': 0},
        'waterGardenRelay': {'val': 0},
        'waterSideRelay': {'val': 0},
        'waterEastRelay': {'val': 0},
        'waterWestRelay': {'val': 0},
        'waterSouthRelay': {'val': 0},
        'windSpeed': {'val': 0},
        'rainFlow': {'val': 0}
    },
    'safety': {
        'ping': {'val': 0, 'fct': fct.timeout_reset},
        'moveCoridorContact': {'val': 0, 'type': ["move"]},
        'moveDiningContact': {'val': 0, 'type': ["move"]},
        'moveEntryContact': {'val': 0, 'type': ["move"]},
        'doorEntryContact': {'val': 0, 'type': ["alarm"]},
        'lightAlarm': {'val': 0},
        'moveRelay': {'val': 0},
        'buzzerRelay': {'val': 0},
        'heaterRelay': {'val': 0},
        'out2Relay': {'val': 0},
        'out3Relay': {'val': 0},
        'out4Relay': {'val': 0}
    },
    'dining': {
        'ping': {'val': 0, 'fct': fct.timeout_reset},
        'windowShutterButton': {'val': 1, 'fct': fct.call_url_if_val_change,
                                'url': [
                                    'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=192',
                                    'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=190',
                                    'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=191'
                                ]},
        'windowWindowContact': {'val': 0, 'type': ["alarm"]},
        'windowShutterContact': {'val': 0, 'type': ["alarm"]},
        'doorWindowContact': {'val': 0, 'type': ["alarm"]},
        'doorShutterContact': {'val': 0, 'type': ["alarm"]},
        'tvShutterContact': {'val': 0, 'type': ["alarm"]},
        'lightRelay': {'val': 0},
        'tempSensors': {'2892A7FB05000073': {'val': 20.0, 'name': "c0", 'type': 'temp'},
                        '28D2AFFB05000038': {'val': 20.0, 'name': "c1", 'type': 'temp'},
                        '2813CEFB0500004C': {'val': 20.0, 'name': "c2", 'type': 'temp'},
                        '28FF6CC7070000BD': {'val': 20.0, 'name': "c3", 'type': 'temp'}
                       }
    },
    'kitchen': {
        'ping': {'val': 0, 'fct': fct.timeout_reset},
        'windowWindowContact': {'val': 0, 'type': ["alarm"]},
        'windowShutterContact': {'val': 0, 'type': ["alarm"]},
        'doorWindowContact': {'val': 0, 'type': ["alarm"]},
        'doorShutterContact': {'val': 0, 'type': ["alarm"]},
        'doorShutterButton': {'val': 1, 'fct': fct.call_url_if_val_change,
                              'url': [
                                  'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=202',
                                  'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=200',
                                  'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=201'
                              ]},
        'lightRelay': {'val': 0},
        'entryRelay': {'val': 0},
        'tempSensors': {'28F4A156070000E5': {'val': 20.0, 'name': "c0", 'type': 'temp'},
                        '28121AAF070000A3': {'val': 20.0, 'name': "c1", 'type': 'temp'},
                        '28BAACFB05000014': {'val': 20.0, 'name': "c2", 'type': 'temp'},
                        '285FA8FB050000C9': {'val': 20.0, 'name': "c3", 'type': 'temp'}
                       }
    },
    'bedroom': {
        'ping': {'val': 0, 'fct': fct.timeout_reset},
        'parentsShutterButton': {'val': 1, 'fct': fct.call_url_if_val_change,
                                 'url': [
                                     'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=167',
                                     'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=165',
                                     'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=166'
                                 ]},
        'parentsWindowContact': {'val': 0, 'type': ["alarm"]},
        'parentsShutterContact': {'val': 0, 'type': ["alarm"]},
        'ellisShutterButton': {'val': 1, 'fct': fct.call_url_if_val_change,
                               'url': [
                                   'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=162',
                                   'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=160',
                                   'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=161'
                               ]},
        'ellisWindowContact': {'val': 0, 'type': ["alarm"]},
        'ellisShutterContact': {'val': 0, 'type': ["alarm"]},
        'desktopShutterButton': {'val': 1, 'fct': fct.call_url_if_val_change,
                                 'url': [
                                     'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=172',
                                     'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=170',
                                     'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=171'
                                 ]},
        'desktopWindowContact': {'val': 0, 'type': ["alarm"]},
        'desktopShutterContact': {'val': 0, 'type': ["alarm"]},
        'basementWindowContact': {'val': 0, 'type': ["alarm"]},
        'basementShutterContact': {'val': 0, 'type': ["alarm"]},
        'lightRelay': {'val': 0},
        'tempSensors': {'287CB2FB050000E7': {'val': 20.0, 'name': "parents", 'type': 'temp'},
                        '2861CCFB05000039': {'val': 20.0, 'name': "desktop", 'type': 'temp'},
                        '2841825707000030': {'val': 20.0, 'name': "ellis", 'type': 'temp'},
                        '287288AE070000DB': {'val': 20.0, 'name': "bathroom", 'type': 'temp'},
                        '28C6A9FB05000023': {'val': 20.0, 'name': "corridor", 'type': 'temp'},
                        '28EF9B560700007F': {'val': 20.0, 'name': "basement", 'type': 'temp'}
                       }
    }
})


alarm_initial_status = copy.deepcopy(acq)
alarm_is_enabled = False
alarm_triggered = False
alarm_timeout = 0
alarm_stopped = False
presence_is_enabled = False
move_is_enabled = True


def print_temp(elts):
    """
        Print all temperature values
    """
    msg = ""
    for node, value in elts.items():
        if isinstance(value, dict) is True:
            if 'val' in value:
                if 'type'in value:
                    if value['type'] == "temp":
                        node_name = node
                        if 'name' in value:
                            node_name = value['name']
                        msg = msg + " " + node_name + "=" + str(value['val'])
            else:
                msg = msg + print_temp(value)
    return msg


run_loop = 0
log_msg = ""

def run():
    """
        Cycle execution to update log file
    """
    global run_loop
    global log_msg
    try:
        flog = open("/dev/shm/lbGate.settings", "w")
        msg = "###########################\n"
        msg = msg + "### " + time.strftime('%Y/%m/%d %H:%M:%S') + " ###\n"
        msg = msg + "# contact_status =\n"
        msg = msg + "    # node contact = current value | alarm value\n"
        for node_name, node_value in acq.items():
            for sensor_name, sensor_value in node_value.items():
                if 'type' in sensor_value:
                    if "alarm" in sensor_value['type']:
                        msg = msg + "    " + node_name.rjust(7) + " " + sensor_name.rjust(22) + " = " + str(sensor_value['val']) + " | " + str(alarm_initial_status[node_name][sensor_name]['val']) + "\n"
        msg = msg + "# move_status =\n"
        for node_name, node_value in acq.items():
            for sensor_name, sensor_value in node_value.items():
                if 'type' in sensor_value:
                    if "move" in sensor_value['type']:
                        msg = msg + "    " + node_name.rjust(7) + " " + sensor_name.rjust(22) + " = " + str(sensor_value['val']) + "\n"
        msg = msg + "# alarm_is_enabled = " + str(alarm_is_enabled) + "\n"
        msg = msg + "# alarm_triggered = " + str(alarm_triggered) + "\n"
        msg = msg + "# alarm_timeout = " + str(alarm_timeout) + "\n"
        msg = msg + "# alarm_stopped = " + str(alarm_stopped) + "\n"
        msg = msg + "# presence_is_enabled = " + str(presence_is_enabled) + "\n"
        msg = msg + "# move_is_enabled = " + str(move_is_enabled) + "\n"
        msg = msg + "# node_list =\n"
        msg = msg + "    #  node =   is_open |  open_cnt |    cmd_rx |   ping_tx |   ping_rx |        wd | Max/" + str(MAX_NODE_ERRORS) + " | read_iter\n"
        for key, value in node_list.items():
            msg = msg + "    " + key.rjust(7) + " = " + str(value.is_open()).rjust(9) + " | " + str(value.open_cnt).rjust(9) + " | " + str(value.cmd_rx_cnt).rjust(9) + " | " + str(value.ping_tx_cnt).rjust(9) + " | " + str(value.ping_rx_cnt).rjust(9) + " | " + str(value.error_cnt).rjust(9) + " | " + str(value.error_cnt_max).rjust(9) + " | " + str(value.read_iter).rjust(9) + "\n"
        for key, value in acq.items():
            msg_temp = print_temp(value)
            if msg_temp != '':
                msg = msg + key + " temp:" + msg_temp + "\n"
        msg = msg + "- run_loop = " + str(run_loop) + "\n"
        log_msg = msg
        flog.write(msg)
        flog.close()
    except Exception as ex:
        fct.log_exception(ex)
    run_loop = run_loop + 1


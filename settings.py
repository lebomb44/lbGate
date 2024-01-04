#! /usr/bin/env python3
# coding: utf-8


""" LbGate settings, global variables"""


import time
import copy

import fct
import lbserial
import lbrts
import lbups


HTTPD_PORT = 8444
MAX_NODE_ERRORS = 10000

ALARM_NAME_URL = ('http://localhost/core/api/jeeApi.php?'
                  'plugin=virtual&type=event&'
                  'apikey=IfTprumNYRf0MxCtGlhXGxAB3GPXpHl0&'
                  'id=277&value=')

HOSTNAME = "Niepce"

node_list = dict(
    bedroom=lbserial.Serial('bedroom'),
    safety=lbserial.Serial('safety'),
    dining=lbserial.Serial('dining'),
    kitchen=lbserial.Serial('kitchen'),
    ext=lbserial.Serial('ext'),
    entry=lbserial.Serial('entry'),
    heatpump=lbserial.Serial('heatpump'))

rts=lbrts.Rts("rfplayer")
ups=lbups.Ups("usb/hiddev0")

acq = dict({
    'heatpump': {
        'ping': {'val': 0, 'fct': "timeout_reset"},
        'power': {'val': "UNKNOWN"},
        'mode': {'val': "UNKNOWN"},
        'temp': {'val': 0.0},
        'fanspeed': {'val': "UNKNOWN"},
        'vane': {'val': 0},
        'widevane': {'val': "UNKNOWN"},
        'isee': {'val': 0},
        'roomtemp': {'val': 0.0},
        'operating': {'val': 0}
    },
    'entry': {
        'ping': {'val': 0, 'fct': "timeout_reset"},
        'nfcTag': {'val': 0, 'fct': "nfcTag"}
    },
    'ext': {
        'ping': {'val': 0, 'fct': "timeout_reset"},
        'waterMainRelay': {'val': 0},
        'waterGardenRelay': {'val': 0},
        'waterSideRelay': {'val': 0},
        'waterEastRelay': {'val': 0},
        'waterWestRelay': {'val': 0},
        'waterSouthRelay': {'val': 0},
        'windSpeed': {'val': 0},
        'rainFlow': {'val': 0},
        'tempSensors': {'287979C8070000D1': {'val': 20.0, 'name': "antenna", 'type': ["temp"]}}
    },
    'safety': {
        'ping': {'val': 0, 'fct': "timeout_reset"},
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
        'ping': {'val': 0, 'fct': "timeout_reset"},
        'windowShutterButton': {'val': 1, 'fct': "call_rts_if_val_change",
                                'rts': [
                                    'DIM %4 ID 4 RTS',
                                    'ON ID 4 RTS',
                                    'OFF ID 4 RTS'
                                ]},
        'windowWindowContact': {'val': 0, 'type': ["alarm"]},
        'windowShutterContact': {'val': 0, 'type': ["alarm"]},
        'doorWindowContact': {'val': 0, 'type': ["alarm"]},
        'doorShutterContact': {'val': 0, 'type': ["alarm"]},
        'tvShutterContact': {'val': 0, 'type': ["alarm"]},
        'lightRelay': {'val': 0},
        'tempSensors': {'2892A7FB05000073': {'val': 20.0, 'name': "terrasse", 'type': ["temp"]},
                        '28D2AFFB05000038': {'val': 20.0, 'name': "fixe", 'type': ["temp"]},
                        '2813CEFB0500004C': {'val': 20.0, 'name': "fenetre", 'type': ["temp"]},
                        '28FF6CC7070000BD': {'val': 20.0, 'name': "tv", 'type': ["temp"]}
                       }
    },
    'kitchen': {
        'ping': {'val': 0, 'fct': "timeout_reset"},
        'windowWindowContact': {'val': 0, 'type': ["alarm"]},
        'windowShutterContact': {'val': 0, 'type': ["alarm"]},
        'doorWindowContact': {'val': 0, 'type': ["alarm"]},
        'doorShutterContact': {'val': 0, 'type': ["alarm"]},
        'doorShutterButton': {'val': 1, 'fct': "call_rts_if_val_change",
                              'rts': [
                                  'DIM %4 ID 8 RTS',
                                  'ON ID 8 RTS',
                                  'OFF ID 8 RTS'
                              ]},
        'lightRelay': {'val': 0},
        'entryRelay': {'val': 0},
        'tempSensors': {'28F4A156070000E5': {'val': 20.0, 'name': "telephone", 'type': ["temp"]},
                        '28121AAF070000A3': {'val': 20.0, 'name': "prise", 'type': ["temp"]},
                        '28BAACFB05000014': {'val': 20.0, 'name': "fenetre", 'type': ["temp"]},
                        '285FA8FB050000C9': {'val': 20.0, 'name': "porte", 'type': ["temp"]}
                       }
    },
    'bedroom': {
        'ping': {'val': 0, 'fct': "timeout_reset"},
        'parentsShutterButton': {'val': 1, 'fct': "call_rts_if_val_change",
                                 'rts': [
                                     'DIM %4 ID 16 RTS',
                                     'ON ID 16 RTS',
                                     'OFF ID 16 RTS'
                                 ]},
        'parentsWindowContact': {'val': 0, 'type': ["alarm"]},
        'parentsShutterContact': {'val': 0, 'type': ["alarm"]},
        'ellisShutterButton': {'val': 1, 'fct': "call_rts_if_val_change",
                               'rts': [
                                   'DIM %4 ID 14 RTS',
                                   'ON ID 14 RTS',
                                   'OFF ID 14 RTS'
                               ]},
        'ellisWindowContact': {'val': 0, 'type': ["alarm"]},
        'ellisShutterContact': {'val': 0, 'type': ["alarm"]},
        'desktopShutterButton': {'val': 1, 'fct': "call_rts_if_val_change",
                                 'rts': [
                                     'DIM %4 ID 18 RTS',
                                     'ON ID 18 RTS',
                                     'OFF ID 18 RTS'
                                 ]},
        'desktopWindowContact': {'val': 0, 'type': ["alarm"]},
        'desktopShutterContact': {'val': 0, 'type': ["alarm"]},
        'basementWindowContact': {'val': 0, 'type': ["alarm"]},
        'basementShutterContact': {'val': 0, 'type': ["alarm"]},
        'lightRelay': {'val': 0},
        'tempSensors': {'287CB2FB050000E7': {'val': 20.0, 'name': "parents", 'type': ["temp"]},
                        '2861CCFB05000039': {'val': 20.0, 'name': "desktop", 'type': ["temp"]},
                        '2841825707000030': {'val': 20.0, 'name': "ellis", 'type': ["temp"]},
                        '287288AE070000DB': {'val': 20.0, 'name': "bathroom", 'type': ["temp"]},
                        '28C6A9FB05000023': {'val': 20.0, 'name': "corridor", 'type': ["temp"]},
                        '28EF9B560700007F': {'val': 20.0, 'name': "basement", 'type': ["temp"]}
                       }
    }
})

alarm = dict({
    'initial_status': copy.deepcopy(acq),
    'is_enabled': False,
    'use_move': True,
    'triggered': False,
    'timeout': 0,
    'stopped': False,
    'contacts': 0
})

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
                    if "temp" in value['type']:
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
                        msg = msg + "    " + node_name.rjust(7) + " " + sensor_name.rjust(22) + " = " + str(sensor_value['val']) + " | " + str(alarm['initial_status'][node_name][sensor_name]['val']) + "\n"
        msg = msg + "# move_status =\n"
        for node_name, node_value in acq.items():
            for sensor_name, sensor_value in node_value.items():
                if 'type' in sensor_value:
                    if "move" in sensor_value['type']:
                        msg = msg + "    " + node_name.rjust(7) + " " + sensor_name.rjust(22) + " = " + str(sensor_value['val']) + "\n"
        msg = msg + "# alarm: is_enabled=" + str(alarm['is_enabled']) + " use_move=" + str(alarm['use_move']) + " triggered=" + str(alarm['triggered']) + " timeout=" + str(alarm['timeout']) + " stopped=" + str(alarm['stopped']) + "\n"
        msg = msg + "# presence_is_enabled=" + str(presence_is_enabled) + " move_is_enabled=" + str(move_is_enabled) + "\n"
        msg = msg + "# node_list =\n"
        msg = msg + "    #  node =   is_open |  open_cnt |    cmd_rx |   ping_tx |   ping_rx |        wd | Max/" + str(MAX_NODE_ERRORS) + " | read_iter\n"
        for key, value in node_list.items():
            msg = msg + "    " + key.rjust(7) + " = " + str(value.is_open()).rjust(9) + " | " + str(value.open_cnt).rjust(9) + " | " + str(value.cmd_rx_cnt).rjust(9) + " | " + str(value.ping_tx_cnt).rjust(9) + " | " + str(value.ping_rx_cnt).rjust(9) + " | " + str(value.error_cnt).rjust(9) + " | " + str(value.error_cnt_max).rjust(9) + " | " + str(value.read_iter).rjust(9) + "\n"
        for key, value in acq.items():
            msg_temp = print_temp(value)
            if msg_temp != '':
                msg = msg + key + " temp:" + msg_temp + "\n"
        msg = msg + "# weather = " + "rain=" + str(acq['ext']['rainFlow']['val']) + " wind=" + str(acq['ext']['windSpeed']['val']) + "\n"
        msg = msg + "# ups = " + "port=" + str(ups.port) + " is_open=" + str(ups.is_open()) + " open_cnt=" + str(ups.open_cnt) + " iter=" + str(ups.read_iter) + " loop=" + str(ups.is_loop_enabled) + "\n"
        msg = msg + "- run_loop = " + str(run_loop) + "\n"
        log_msg = msg
        flog.write(msg)
        flog.close()
    except Exception as ex:
        fct.log_exception(ex)
    run_loop = run_loop + 1


#! /usr/bin/env python3
# coding: utf-8


""" LbGate settings, global variables"""


import time
import serial

import fct


HTTPD_PORT = 8444
MAX_NODE_ERRORS = 5000
SMS_URL = ('http://localhost/core/api/jeeApi.php?'
           'apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&'
           'type=cmd&id=288&title=Jeedom&message=')
EMAIL_URL = ('http://localhost/core/api/jeeApi.php?'
             'apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&'
             'type=cmd&id=225&title=Jeedom&message=')


node_list = dict(
    safety={'port': '/dev/safety', 'fd': serial.Serial(), 'errorCnt': 0, 'cmdRxCnt': 0, 'pingTxCnt': 0, 'line': ""},
    dining={'port': '/dev/dining', 'fd': serial.Serial(), 'errorCnt': 0, 'cmdRxCnt': 0, 'pingTxCnt': 0, 'line': ""},
    kitchen={'port': '/dev/kitchen', 'fd': serial.Serial(), 'errorCnt': 0, 'cmdRxCnt': 0, 'pingTxCnt': 0, 'line': ""},
    bedroom={'port': '/dev/bedroom', 'fd': serial.Serial(), 'errorCnt': 0, 'cmdRxCnt': 0, 'pingTxCnt': 0, 'line': ""},
    ext={'port': '/dev/ext', 'fd': serial.Serial(), 'errorCnt': 0, 'cmdRxCnt': 0, 'pingTxCnt': 0, 'line': ""})


for node_serial in node_list:
    node_list[node_serial]['fd'].port = node_list[node_serial]['port']
    node_list[node_serial]['fd'].baudrate = 115200
    node_list[node_serial]['fd'].parity = serial.PARITY_NONE
    node_list[node_serial]['fd'].stopbits = serial.STOPBITS_ONE
    node_list[node_serial]['fd'].bytesize = serial.EIGHTBITS
    node_list[node_serial]['fd'].timeout = 0
    node_list[node_serial]['fd'].xonxoff = False
    node_list[node_serial]['fd'].rtscts = False
    node_list[node_serial]['fd'].dsrdtr = False
    node_list[node_serial]['fd'].writeTimeout = 0.1


jeedom_url = dict({
    'safety ping get': {'fct': fct.timeout_reset, 'url': "safety"},
    'safety moveCoridorContact hk 0':
        {'fct': fct.move_status_set_moving, 'url': "safety moveCoridorContact"},
    'safety moveCoridorContact hk 1':
        {'fct': fct.move_status_set_stated, 'url': "safety moveCoridorContact"},
    'safety moveDiningContact hk 0':
        {'fct': fct.move_status_set_moving, 'url': "safety moveDiningContact"},
    'safety moveDiningContact hk 1':
        {'fct': fct.move_status_set_stated, 'url': "safety moveDiningContact"},
    'safety moveEntryContact hk 0':
        {'fct': fct.move_status_set_moving, 'url': "safety moveEntryContact"},
    'safety moveEntryContact hk 1':
        {'fct': fct.move_status_set_stated, 'url': "safety moveEntryContact"},
    'safety doorEntryContact hk 1': {'fct': fct.contact_status_set_close, 'url': "safety doorEntryContact"},
    'safety doorEntryContact hk 0': {'fct': fct.contact_status_set_open, 'url': "safety doorEntryContact"},
    'safety lightAlarm get 0': {'fct': None, 'url': "safety lightAlarm"},
    'safety lightAlarm get 1': {'fct': None, 'url': "safety lightAlarm"},
    'safety moveRelay get 0': {'fct': None, 'url': "safety moveRelay"},
    'safety moveRelay get 1': {'fct': None, 'url': "safety moveRelay"},
    'safety buzzerRelay get 0': {'fct': None, 'url': "safety buzzerRelay"},
    'safety buzzerRelay get 1': {'fct': None, 'url': "safety buzzerRelay"},
    'safety out1Relay get 0': {'fct': None, 'url': "safety out1Relay"},
    'safety out1Relay get 1': {'fct': None, 'url': "safety out1Relay"},
    'safety out2Relay get 0': {'fct': None, 'url': "safety out2Relay"},
    'safety out2Relay get 1': {'fct': None, 'url': "safety out2Relay"},
    'safety out3Relay get 0': {'fct': None, 'url': "safety out3Relay"},
    'safety out3Relay get 1': {'fct': None, 'url': "safety out3Relay"},
    'safety out4Relay get 0': {'fct': None, 'url': "safety out4Relay"},
    'safety out4Relay get 1': {'fct': None, 'url': "safety out4Relay"},
    'dining ping get': {'fct': fct.timeout_reset, 'url': "dining"},
    'dining windowShutterButton hk 0': {'fct': fct.http_request, 'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=192'},
    'dining windowShutterButton hk 1': {'fct': fct.http_request, 'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=190'},
    'dining windowShutterButton hk 2': {'fct': fct.http_request, 'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=191'},
    'dining windowWindowContact hk 1': {'fct': fct.contact_status_set_close, 'url': "dining windowWindowContact"},
    'dining windowWindowContact hk 0': {'fct': fct.contact_status_set_open, 'url': "dining windowWindowContact"},
    'dining windowShutterContact hk 1': {'fct': fct.contact_status_set_close, 'url': "dining windowShutterContact"},
    'dining windowShutterContact hk 0': {'fct': fct.contact_status_set_open, 'url': "dining windowShutterContact"},
    'dining doorWindowContact hk 1': {'fct': fct.contact_status_set_close, 'url': "dining doorWindowContact"},
    'dining doorWindowContact hk 0': {'fct': fct.contact_status_set_open, 'url': "dining doorWindowContact"},
    'dining doorShutterContact hk 1': {'fct': fct.contact_status_set_close, 'url': "dining doorShutterContact"},
    'dining doorShutterContact hk 0': {'fct': fct.contact_status_set_open, 'url': "dining doorShutterContact"},
    'dining tvShutterContact hk 1': {'fct': fct.contact_status_set_close, 'url': "dining tvShutterContact"},
    'dining tvShutterContact hk 0': {'fct': fct.contact_status_set_open, 'url': "dining tvShutterContact"},
    'dining lightRelay get 1': {'fct': None, 'url': "dining lightRelay"},
    'dining lightRelay get 0': {'fct': None, 'url': "dining lightRelay"},
    'dining tempSensors hk 2892A7FB05000073': {'fct': fct.temp_set, 'url': "dining c0Temp"},
    'dining tempSensors hk 28D2AFFB05000038': {'fct': fct.temp_set, 'url': "dining c1Temp"},
    'dining tempSensors hk 2813CEFB0500004C': {'fct': fct.temp_set, 'url': "dining c2Temp"},
    'dining tempSensors hk 28FF6CC7070000BD': {'fct': fct.temp_set, 'url': "dining c3Temp"},
    'kitchen ping get': {'fct': fct.timeout_reset, 'url': "kitchen"},
    'kitchen windowWindowContact hk 1': {'fct': fct.contact_status_set_close, 'url': "kitchen windowWindowContact"},
    'kitchen windowWindowContact hk 0': {'fct': fct.contact_status_set_open, 'url': "kitchen windowWindowContact"},
    'kitchen windowShutterContact hk 1': {'fct': fct.contact_status_set_close, 'url': "kitchen windowShutterContact"},
    'kitchen windowShutterContact hk 0': {'fct': fct.contact_status_set_open, 'url': "kitchen windowShutterContact"},
    'kitchen doorShutterButton hk 0': {'fct': fct.http_request,
                                       'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=202'},
    'kitchen doorShutterButton hk 1': {'fct': fct.http_request,
                                       'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=200'},
    'kitchen doorShutterButton hk 2': {'fct': fct.http_request,
                                       'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=201'},
    'kitchen doorWindowContact hk 1': {'fct': fct.contact_status_set_close, 'url': "kitchen doorWindowContact"},
    'kitchen doorWindowContact hk 0': {'fct': fct.contact_status_set_open, 'url': "kitchen doorWindowContact"},
    'kitchen doorShutterContact hk 1': {'fct': fct.contact_status_set_close, 'url': "kitchen doorShutterContact"},
    'kitchen doorShutterContact hk 0': {'fct': fct.contact_status_set_open, 'url': "kitchen doorShutterContact"},
    'kitchen lightRelay get 1': {'fct': None, 'url': "kitchen lightRelay"},
    'kitchen lightRelay get 0': {'fct': None, 'url': "kitchen lightRelay"},
    'kitchen tempSensors hk 28F4A156070000E5': {'fct': fct.temp_set, 'url': "kitchen c0Temp"},
    'kitchen tempSensors hk 28121AAF070000A3': {'fct': fct.temp_set, 'url': "kitchen c1Temp"},
    'kitchen tempSensors hk 28BAACFB05000014': {'fct': fct.temp_set, 'url': "kitchen c2Temp"},
    'kitchen tempSensors hk 285FA8FB050000C9': {'fct': fct.temp_set, 'url': "kitchen c3Temp"},
    'bedroom ping get': {'fct': fct.timeout_reset, 'url': "bedroom"},
    'bedroom parentsShutterButton hk 0': {'fct': fct.http_request,
                                          'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=167'},
    'bedroom parentsShutterButton hk 1': {'fct': fct.http_request,
                                          'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=165'},
    'bedroom parentsShutterButton hk 2': {'fct': fct.http_request,
                                          'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=166'},
    'bedroom parentsWindowContact hk 1': {'fct': fct.contact_status_set_close, 'url': "bedroom parentsWindowContact"},
    'bedroom parentsWindowContact hk 0': {'fct': fct.contact_status_set_open, 'url': "bedroom parentsWindowContact"},
    'bedroom parentsShutterContact hk 1': {'fct': fct.contact_status_set_close, 'url': "bedroom parentsShutterContact"},
    'bedroom parentsShutterContact hk 0': {'fct': fct.contact_status_set_open, 'url': "bedroom parentsShutterContact"},
    'bedroom ellisShutterButton hk 0': {'fct': fct.http_request,
                                        'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=162'},
    'bedroom ellisShutterButton hk 1': {'fct': fct.http_request,
                                        'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=160'},
    'bedroom ellisShutterButton hk 2': {'fct': fct.http_request,
                                        'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=161'},
    'bedroom ellisWindowContact hk 1': {'fct': fct.contact_status_set_close, 'url': "bedroom ellisWindowContact"},
    'bedroom ellisWindowContact hk 0': {'fct': fct.contact_status_set_open, 'url': "bedroom ellisWindowContact"},
    'bedroom ellisShutterContact hk 1': {'fct': fct.contact_status_set_close, 'url': "bedroom ellisShutterContact"},
    'bedroom ellisShutterContact hk 0': {'fct': fct.contact_status_set_open, 'url': "bedroom ellisShutterContact"},
    'bedroom desktopShutterButton hk 0': {'fct': fct.http_request,
                                          'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=172'},
    'bedroom desktopShutterButton hk 1': {'fct': fct.http_request,
                                          'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=170'},
    'bedroom desktopShutterButton hk 2': {'fct': fct.http_request,
                                          'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=171'},
    'bedroom desktopWindowContact hk 1': {'fct': fct.contact_status_set_close, 'url': "bedroom desktopWindowContact"},
    'bedroom desktopWindowContact hk 0': {'fct': fct.contact_status_set_open, 'url': "bedroom desktopWindowContact"},
    'bedroom desktopShutterContact hk 1': {'fct': fct.contact_status_set_close, 'url': "bedroom desktopShutterContact"},
    'bedroom desktopShutterContact hk 0': {'fct': fct.contact_status_set_open, 'url': "bedroom desktopShutterContact"},
    'bedroom basementWindowContact hk 1': {'fct': fct.contact_status_set_close, 'url': "bedroom basementWindowContact"},
    'bedroom basementWindowContact hk 0': {'fct': fct.contact_status_set_open, 'url': "bedroom basementWindowContact"},
    'bedroom basementShutterContact hk 1': {'fct': fct.contact_status_set_close, 'url': "bedroom basementShutterContact"},
    'bedroom basementShutterContact hk 0': {'fct': fct.contact_status_set_open, 'url': "bedroom basementShutterContact"},
    'bedroom lightRelay get 1': {'fct': None, 'url': "bedroom lightRelay"},
    'bedroom lightRelay get 0': {'fct': None, 'url': "bedroom lightRelay"},
    'bedroom tempSensors hk 287CB2FB050000E7': {'fct': fct.temp_set, 'url': "bedroom parentsTemp"},
    'bedroom tempSensors hk 2861CCFB05000039': {'fct': fct.temp_set, 'url': "bedroom desktopTemp"},
    'bedroom tempSensors hk 2841825707000030': {'fct': fct.temp_set, 'url': "bedroom ellisTemp"},
    'bedroom tempSensors hk 287288AE070000DB': {'fct': fct.temp_set, 'url': "bedroom bathroomTemp"},
    'bedroom tempSensors hk 28C6A9FB05000023': {'fct': fct.temp_set, 'url': "bedroom corridorTemp"},
    'bedroom tempSensors hk 28EF9B560700007F': {'fct': fct.temp_set, 'url': "bedroom basementTemp"},
    'ext ping get': {'fct': fct.timeout_reset, 'url': "ext"},
    'ext waterMainRelay get 0': {'fct': None, 'url': "ext waterMainRelay"},
    'ext waterMainRelay get 1': {'fct': None, 'url': "ext waterMainRelay"},
    'ext waterGardenRelay get 0': {'fct': None, 'url': "ext waterGardenRelay"},
    'ext waterGardenRelay get 1': {'fct': None, 'url': "ext waterGardenRelay"},
    'ext waterSideRelay get 0': {'fct': None, 'url': "ext waterSideRelay"},
    'ext waterSideRelay get 1': {'fct': None, 'url': "ext waterSideRelay"},
    'ext waterEastRelay get 0': {'fct': None, 'url': "ext waterEastRelay"},
    'ext waterEastRelay get 1': {'fct': None, 'url': "ext waterEastRelay"},
    'ext waterWestRelay get 0': {'fct': None, 'url': "ext waterWestRelay"},
    'ext waterWestRelay get 1': {'fct': None, 'url': "ext waterWestRelay"},
    'ext waterSouthRelay get 0': {'fct': None, 'url': "ext waterSouthRelay"},
    'ext waterSouthRelay get 1': {'fct': None, 'url': "ext waterSouthRelay"}
})


contact_status = dict({
    'dining windowWindowContact': True,
    'dining windowShutterContact': True,
    'dining doorWindowContact': True,
    'dining doorShutterContact': True,
    'dining tvShutterContact': True,
    'kitchen windowWindowContact': True,
    'kitchen windowShutterContact': True,
    'kitchen doorWindowContact': True,
    'kitchen doorShutterContact': True,
    'bedroom parentsWindowContact': True,
    'bedroom parentsShutterContact': True,
    'bedroom ellisWindowContact': True,
    'bedroom ellisShutterContact': True,
    'bedroom desktopWindowContact': True,
    'bedroom desktopShutterContact': True,
    'bedroom basementWindowContact': True,
    'bedroom basementShutterContact': True,
    'safety doorEntryContact': True
})


move_status = dict({
    'safety moveCoridorContact': True,
    'safety moveDiningContact': True,
    'safety moveEntryContact': True
})


temp = dict({})


alarm_initial_status = contact_status.copy()
alarm_is_enabled = False
alarm_triggered = False
alarm_timeout = 0
presence_is_enabled = False
move_is_enabled = True


runLoop = 0


def run():
    global runLoop
    try:
        f = open("/dev/shm/lbGate.settings", "w")
        f.write("########################### pySerial=" + serial.VERSION + "\n")
        f.write("### " + time.strftime('%Y/%m/%d %H:%M:%S') + " ###\n")
        f.write("# contact_status =\n")
        f.write("    # node contact = current value | alarm value\n")
        for key, value in contact_status.items():
            f.write("    " + key + " = " + str(value) + " | " + str(alarm_initial_status[key]) + "\n")
        f.write("# move_status =\n")
        for key, value in move_status.items():
            f.write("    " + key + " = " + str(value) + "\n")
        f.write("# alarm_is_enabled = " + str(alarm_is_enabled) + "\n")
        f.write("# alarm_triggered = " + str(alarm_triggered) + "\n")
        f.write("# alarm_timeout = " + str(alarm_timeout) + "\n")
        f.write("# presence_is_enabled = " + str(presence_is_enabled) + "\n")
        f.write("# move_is_enabled = " + str(move_is_enabled) + "\n")
        f.write("# node_list =\n")
        f.write("    # node = isOpen | cmdRx | pingTx | errors\n")
        for key, value in node_list.items():
            f.write("    " + key + " = " + str(value['fd'].isOpen()) + " | " + str(value['cmdRxCnt']) + " | " + str(value['pingTxCnt']) + " | " + str(value['errorCnt']) + "\n")
        f.write("- runLoop = " + str(runLoop) + "\n")
        f.write("\n")
        f.close()
    except:
        pass
    runLoop = runLoop + 1


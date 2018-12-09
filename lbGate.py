#! /usr/bin/env python3
# coding: utf-8

import http.server
import threading
import time
import requests
import serial
import signal
import sys
import urllib.parse
import datetime

nodeList = dict(
    safety={'port': '/dev/safety', 'fd': serial.Serial(), 'errorCnt': 0, 'cmdCnt': 0},
    dining={'port': '/dev/dining', 'fd': serial.Serial(), 'errorCnt': 0, 'cmdCnt': 0},
    kitchen={'port': '/dev/kitchen', 'fd': serial.Serial(), 'errorCnt': 0, 'cmdCnt': 0},
    bedroom={'port': '/dev/bedroom', 'fd': serial.Serial(), 'errorCnt': 0, 'cmdCnt': 0},
    ext={'port': '/dev/ext', 'fd': serial.Serial(), 'errorCnt': 0, 'cmdCnt': 0})

for nodeSerial in nodeList:
    nodeList[nodeSerial]['fd'].port = nodeList[nodeSerial]['port']
    nodeList[nodeSerial]['fd'].baudrate = 115200
    nodeList[nodeSerial]['fd'].parity = serial.PARITY_NONE
    nodeList[nodeSerial]['fd'].stopbits = serial.STOPBITS_ONE
    nodeList[nodeSerial]['fd'].bytesize = serial.EIGHTBITS
    nodeList[nodeSerial]['fd'].timeout = 0.01
    nodeList[nodeSerial]['fd'].xonxoff = False
    nodeList[nodeSerial]['fd'].rtscts = False
    nodeList[nodeSerial]['fd'].dsrdtr = False
    nodeList[nodeSerial]['fd'].writeTimeout = 0.1

MAX_NODE_ERRORS = 5000
HTTPD_PORT = 8444
SMS_URL = 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=288&title=Jeedom&message='
EMAIL_URL = 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=225&title=Jeedom&message='


def httpRequest(url):
    try:
        log("URL call: " + url)
        requests.get(url, timeout=0.1)
    except:
        pass


def alarmStatus_setClose(key):
    global alarmStatus
    alarmStatus[key] = True


def alarmStatus_setOpen(key):
    global alarmStatus
    alarmStatus[key] = False


def moveStatus_setStated(key):
    global moveStatus
    moveStatus[key] = True


def moveStatus_setMoving(key):
    global moveStatus
    moveStatus[key] = False


def timeoutCheck(node_):
    global nodeList
    if MAX_NODE_ERRORS > nodeList[node_]['errorCnt']:
        nodeList[node_]['errorCnt'] += 1
    if MAX_NODE_ERRORS == nodeList[node_]['errorCnt']:
        sendAlert("Timeout on serial node " + node_)
        nodeList[node_]['errorCnt'] += 1


def timeoutReset(node_):
    global nodeList
    # log("### Reset of node " + node_)
    nodeList[node_]['errorCnt'] = 0


jeedomUrl = dict({
    'safety ping get': {'fct': timeoutReset, 'url': "safety"},
    'safety moveCoridorContact hk 0': {'fct': moveStatus_setMoving, 'url': "safety moveCoridorContact"},
    'safety moveCoridorContact hk 1': {'fct': moveStatus_setStated, 'url': "safety moveCoridorContact"},
    'safety moveDiningContact hk 0': {'fct': moveStatus_setMoving, 'url': "safety moveDiningContact"},
    'safety moveDiningContact hk 1': {'fct': moveStatus_setStated, 'url': "safety moveDiningContact"},
    'safety moveEntryContact hk 0': {'fct': moveStatus_setStated, 'url': "safety moveEntryContact"},
    'safety moveEntryContact hk 1': {'fct': moveStatus_setStated, 'url': "safety moveEntryContact"},
    'safety moveRelay get 0': {'fct': None, 'url': "safety moveRelay"},
    'safety moveRelay get 1': {'fct': None, 'url': "safety moveRelay"},
    'safety out0Relay get 0': {'fct': None, 'url': "safety out0Relay"},
    'safety out0Relay get 1': {'fct': None, 'url': "safety out0Relay"},
    'safety out1Relay get 0': {'fct': None, 'url': "safety out1Relay"},
    'safety out1Relay get 1': {'fct': None, 'url': "safety out1Relay"},
    'safety out2Relay get 0': {'fct': None, 'url': "safety out2Relay"},
    'safety out2Relay get 1': {'fct': None, 'url': "safety out2Relay"},
    'safety out3Relay get 0': {'fct': None, 'url': "safety out3Relay"},
    'safety out3Relay get 1': {'fct': None, 'url': "safety out3Relay"},
    'safety out4Relay get 0': {'fct': None, 'url': "safety out4Relay"},
    'safety out4Relay get 1': {'fct': None, 'url': "safety out4Relay"},
    'dining ping get': {'fct': timeoutReset, 'url': "dining"},
    'dining windowShutterButton hk 0': {'fct': httpRequest,
                                        'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=192'},
    'dining windowShutterButton hk 1': {'fct': httpRequest,
                                        'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=190'},
    'dining windowShutterButton hk 2': {'fct': httpRequest,
                                        'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=191'},
    'dining windowWindowContact hk 1': {'fct': alarmStatus_setClose, 'url': "dining windowWindowContact"},
    'dining windowWindowContact hk 0': {'fct': alarmStatus_setOpen, 'url': "dining windowWindowContact"},
    'dining windowShutterContact hk 1': {'fct': alarmStatus_setClose, 'url': "dining windowShutterContact"},
    'dining windowShutterContact hk 0': {'fct': alarmStatus_setOpen, 'url': "dining windowShutterContact"},
    'dining doorWindowContact hk 1': {'fct': alarmStatus_setClose, 'url': "dining doorWindowContact"},
    'dining doorWindowContact hk 0': {'fct': alarmStatus_setOpen, 'url': "dining doorWindowContact"},
    'dining doorShutterContact hk 1': {'fct': alarmStatus_setClose, 'url': "dining doorShutterContact"},
    'dining doorShutterContact hk 0': {'fct': alarmStatus_setOpen, 'url': "dining doorShutterContact"},
    'dining tvShutterContact hk 1': {'fct': alarmStatus_setClose, 'url': "dining tvShutterContact"},
    'dining tvShutterContact hk 0': {'fct': alarmStatus_setOpen, 'url': "dining tvShutterContact"},
    'dining lightRelay get 1': {'fct': None, 'url': "dining lightRelay"},
    'dining lightRelay get 0': {'fct': None, 'url': "dining lightRelay"},
    'kitchen ping get': {'fct': timeoutReset, 'url': "kitchen"},
    'kitchen windowWindowContact hk 1': {'fct': alarmStatus_setClose, 'url': "kitchen windowWindowContact"},
    'kitchen windowWindowContact hk 0': {'fct': alarmStatus_setOpen, 'url': "kitchen windowWindowContact"},
    'kitchen windowShutterContact hk 1': {'fct': alarmStatus_setClose, 'url': "kitchen windowShutterContact"},
    'kitchen windowShutterContact hk 0': {'fct': alarmStatus_setOpen, 'url': "kitchen windowShutterContact"},
    'kitchen doorShutterButton hk 0': {'fct': httpRequest,
                                       'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=202'},
    'kitchen doorShutterButton hk 1': {'fct': httpRequest,
                                       'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=200'},
    'kitchen doorShutterButton hk 2': {'fct': httpRequest,
                                       'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=201'},
    'kitchen doorWindowContact hk 1': {'fct': alarmStatus_setClose, 'url': "kitchen doorWindowContact"},
    'kitchen doorWindowContact hk 0': {'fct': alarmStatus_setOpen, 'url': "kitchen doorWindowContact"},
    'kitchen doorShutterContact hk 1': {'fct': alarmStatus_setClose, 'url': "kitchen doorShutterContact"},
    'kitchen doorShutterContact hk 0': {'fct': alarmStatus_setOpen, 'url': "kitchen doorShutterContact"},
    'kitchen lightRelay get 1': {'fct': None, 'url': "kitchen lightRelay"},
    'kitchen lightRelay get 0': {'fct': None, 'url': "kitchen lightRelay"},
    'bedroom ping get': {'fct': timeoutReset, 'url': "bedroom"},
    'bedroom parentsShutterButton hk 0': {'fct': httpRequest,
                                          'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=167'},
    'bedroom parentsShutterButton hk 1': {'fct': httpRequest,
                                          'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=165'},
    'bedroom parentsShutterButton hk 2': {'fct': httpRequest,
                                          'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=166'},
    'bedroom parentsWindowContact hk 1': {'fct': alarmStatus_setClose, 'url': "bedroom parentsWindowContact"},
    'bedroom parentsWindowContact hk 0': {'fct': alarmStatus_setOpen, 'url': "bedroom parentsWindowContact"},
    'bedroom parentsShutterContact hk 1': {'fct': alarmStatus_setClose, 'url': "bedroom parentsShutterContact"},
    'bedroom parentsShutterContact hk 0': {'fct': alarmStatus_setOpen, 'url': "bedroom parentsShutterContact"},
    'bedroom ellisShutterButton hk 0': {'fct': httpRequest,
                                        'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=162'},
    'bedroom ellisShutterButton hk 1': {'fct': httpRequest,
                                        'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=160'},
    'bedroom ellisShutterButton hk 2': {'fct': httpRequest,
                                        'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=161'},
    'bedroom ellisWindowContact hk 1': {'fct': alarmStatus_setClose, 'url': "bedroom ellisWindowContact"},
    'bedroom ellisWindowContact hk 0': {'fct': alarmStatus_setOpen, 'url': "bedroom ellisWindowContact"},
    'bedroom ellisShutterContact hk 1': {'fct': alarmStatus_setClose, 'url': "bedroom ellisShutterContact"},
    'bedroom ellisShutterContact hk 0': {'fct': alarmStatus_setOpen, 'url': "bedroom ellisShutterContact"},
    'bedroom desktopShutterButton hk 0': {'fct': httpRequest,
                                          'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=172'},
    'bedroom desktopShutterButton hk 1': {'fct': httpRequest,
                                          'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=170'},
    'bedroom desktopShutterButton hk 2': {'fct': httpRequest,
                                          'url': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=171'},
    'bedroom desktopWindowContact hk 1': {'fct': alarmStatus_setClose, 'url': "bedroom desktopWindowContact"},
    'bedroom desktopWindowContact hk 0': {'fct': alarmStatus_setOpen, 'url': "bedroom desktopWindowContact"},
    'bedroom desktopShutterContact hk 1': {'fct': alarmStatus_setClose, 'url': "bedroom desktopShutterContact"},
    'bedroom desktopShutterContact hk 0': {'fct': alarmStatus_setOpen, 'url': "bedroom desktopShutterContact"},
    'bedroom lightRelay get 1': {'fct': None, 'url': "bedroom lightRelay"},
    'bedroom lightRelay get 0': {'fct': None, 'url': "bedroom lightRelay"},
    'ext ping get': {'fct': timeoutReset, 'url': "ext"},
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

alarmStatus = dict({
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
    'bedroom desktopShutterContact': True
})

moveStatus = dict({
    'safety moveCoridorContact': True,
    'safety moveDiningContact': True,
    'safety moveEntryContact': True
})

alarmInitialStatus = alarmStatus.copy()
alarmIsEnabled = False
alarmTriggered = False
alarmTimeout = 0
presenceIsEnabled = False
moveIsEnabled = True


def log(msg):
    print(time.strftime('%Y/%m/%d %H:%M:%S: ') + msg)


def sendSMS(msg):
    log("Send SMS: " + msg)
    httpRequest(SMS_URL + urllib.parse.quote(msg))
    pass


def sendEmail(msg):
    log("Send EMAIL: " + msg)
    httpRequest(EMAIL_URL + urllib.parse.quote(msg))
    pass


def sendAlert(msg):
    sendSMS(msg)
    sendEmail(msg)


def writeSerial(node_, msg):
    global nodeList
    if nodeList[node_]['fd'].isOpen() is True:
        nodeList[node_]['fd'].write(("\n\n" + node_ + " " + msg + "\n").encode('utf-8'))
        # log("Write ping to node " + node)
        nodeList[node_]['fd'].flushOutput()


class Serial2Http(threading.Thread):
    def __init__(self, name):
        self.is_loopEnabled = True
        threading.Thread.__init__(self, name=name)

    def run(self):
        global nodeList
        global alarmStatus
        global alarmInitialStatus
        global alarmIsEnabled
        global alarmTriggered
        global alarmTimeout
        global presenceIsEnabled
        global moveStatus
        global moveIsEnabled
        loopNb = 0
        moveTimeout = 0
        while self.is_loopEnabled is True:
            for node in nodeList:
                try:
                    if 0 == loopNb % 100:
                        if nodeList[node]['fd'].isOpen() is False:
                            log("Opening " + nodeList[node]['fd'].port)
                            # log(nodeList[node]['fd'].get_settings())
                            nodeList[nodeSerial]['fd'].baudrate = 9600
                            nodeList[node]['fd'].open()
                            time.sleep(0.1)
                            nodeList[node]['fd'].close()
                            nodeList[nodeSerial]['fd'].baudrate = 115200
                            nodeList[node]['fd'].open()
                            time.sleep(0.1)
                            nodeList[node]['fd'].flushInput()
                    if nodeList[node]['fd'].isOpen() is True:
                        if 0 < nodeList[node]['fd'].inWaiting():
                            line = nodeList[node]['fd'].readline().decode("utf-8").rstrip()
                            if "" != line:
                                if line in jeedomUrl:
                                    if jeedomUrl[line]['fct'] is not None:
                                        # log("Serial CMD=" + line)
                                        jeedomUrl[line]['fct'](jeedomUrl[line]['url'])
                                        nodeList[node]['cmdCnt'] += 1
                                else:
                                    lineArray = line.split(" ")
                                    if 2 < len(lineArray):
                                        cmd = lineArray[0]
                                        for token in lineArray[1:-1]:
                                            cmd = cmd + " " + token
                                        if cmd in jeedomUrl:
                                            if jeedomUrl[cmd]['fct'] is not None:
                                                # log("Serial CMD-1=" + line + " (" + cmd + ")")
                                                jeedomUrl[cmd]['fct'](jeedomUrl[cmd]['url'])
                                                nodeList[node]['cmdCnt'] += 1
                                        else:
                                            log("ERROR: Serial CMD '" + line + "' (" + cmd + ") not found !")
                                    else:
                                        log("ERROR: Serial CMD '" + line + "' not found and too short")
                        if 0 == loopNb % 500:
                            writeSerial(node, "ping get")
                except Exception as e:
                    log("ERROR Exception: " + str(e))
                    nodeList[node]['fd'].close()
                timeoutCheck(node)
            if alarmIsEnabled is True:
                if alarmTriggered is True:
                    if 0 == loopNb % 50:
                        if 10*60 < alarmTimeout:
                            alarmTriggered = False
                            writeSerial("safety", "buzzerRelay set 0")
                        else:
                            alarmTimeout = alarmTimeout + 1
                            writeSerial("safety", "buzzerRelay set 1")
                else:
                    if alarmStatus != alarmInitialStatus:
                        msg = ""
                        for sensor in alarmStatus:
                            if alarmStatus[sensor] != alarmInitialStatus[sensor]:
                                msg += sensor + "=" + alarmStatus[sensor] + ", "
                        alarmTriggered = True
                        alarmTimeout = 0
                        writeSerial("safety", "buzzerRelay set 1")
                        sendAlert("ALARM contact: " + msg)
                    elif moveIsEnabled is True:
                        for sensor in moveStatus:
                            if moveStatus[sensor] is False:
                                alarmTriggered = True
                                alarmTimeout = 0
                                writeSerial("safety", "buzzerRelay set 1")
                                sendAlert("ALARM move: " + sensor)
            else:
                alarmInitialStatus = alarmStatus.copy()
            if moveIsEnabled is True:
                if 0 == loopNb % 50:
                    try:
                        writeSerial("safety", "moveRelay set 1")
                    except Exception as e:
                        log("ERROR Exception: " + str(e))
                    if datetime.datetime.now().hour >= 23 or datetime.datetime.now().hour <= 6:
                        for sensor in moveStatus:
                            if moveStatus[sensor] is False:
                                if "safety moveCoridorContact" == sensor:
                                    writeSerial("bedroom", "lightRelay set 1")
                                    moveTimeout = 0
                                elif "safety moveDiningContact" == sensor:
                                    writeSerial("dining", "lightRelay set 1")
                                    moveTimeout = 0
                                elif "safety moveEntryContact" == sensor:
                                    writeSerial("kitchen", "lightRelay set 0")
                    if 60 < moveTimeout:
                        writeSerial("bedroom", "lightRelay set 0")
                        writeSerial("dining", "lightRelay set 0")
                        writeSerial("kitchen", "lightRelay set 0")
                    else:
                        moveTimeout = moveTimeout + 1
            else:
                if 0 == loopNb % 50:
                    try:
                        writeSerial("safety", "moveRelay set 0")
                    except Exception as e:
                        log("ERROR Exception: " + str(e))
            loopNb += 1
            if 1000000 <= loopNb:
                loopNb = 0
            time.sleep(0.01)

    def stop(self):
        log("Stopping serial2http thread...")
        self.is_loopEnabled = False
        time.sleep(2.0)
        log("Closing all serial nodes...")
        global nodeList
        for node in nodeList:
            try:
                if nodeList[node]['fd'].isOpen() is True:
                    nodeList[node]['fd'].close()
            except Exception as e:
                log("ERROR Exception while closing " + nodeList[node]['port'] + " : " + str(e))


class CustomHandler(http.server.BaseHTTPRequestHandler):
    def ok200(self, resp: str):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write((time.strftime('%Y/%m/%d %H:%M:%S: ') + resp).encode())

    def error404(self, resp: str):
        self.send_response(404)
        self.end_headers()
        self.wfile.write((time.strftime('%Y/%m/%d %H:%M:%S: ') + resp).encode())

    def do_GET(self):
        global nodeList
        global alarmStatus
        global alarmIsEnabled
        global alarmTriggered
        global alarmTimeout
        global presenceIsEnabled
        global moveIsEnabled
        global moveStatus
        urlTokens = self.path.split('/')
        urlTokensLen = len(urlTokens)
        log(str(urlTokens))
        if 1 < urlTokensLen:
            api = urlTokens[1]
            if "api" == api:
                if 2 < urlTokensLen:
                    node = urlTokens[2]
                    if node in nodeList:
                        if 3 < urlTokensLen:
                            cmd = node + " " + urlTokens[3]
                            if 4 < urlTokensLen:
                                for token in urlTokens[4:]:
                                    cmd = cmd + " " + token
                            nodeList[node]['fd'].write(("\n\n" + cmd + "\n\n").encode('utf-8'))
                            nodeList[node]['fd'].flush()
                            self.ok200(cmd)
                        else:
                            self.error404("No command for node: " + node)
                    elif "lbgate" == node:
                        if 3 < urlTokensLen:
                            if "alarm" == urlTokens[3]:
                                if 4 < urlTokensLen:
                                    if "enable" == urlTokens[4]:
                                        alarmIsEnabled = True
                                        alarmTriggered = False
                                        self.ok200("Alarm is enabled: " +
                                                   "<br/>" + "Contacts = " + str(alarmStatus) +
                                                   "<br/>" + "Move = " + str(moveStatus))
                                    elif "disable" == urlTokens[4]:
                                        alarmIsEnabled = False
                                        alarmTriggered = False
                                        self.ok200("Alarm is disabled")
                                    else:
                                        self.ok200("Alarm is = " + str(alarmIsEnabled) +
                                                   "<br/>Trigger = " + str(alarmTriggered) +
                                                   "<br/>Timer = " + str(alarmTimeout) +
                                                   "<br/>Contacts = " + str(alarmStatus) +
                                                   "<br/>Move = " + str(moveStatus))
                                else:
                                    self.ok200("Alarm is = " + str(alarmIsEnabled) +
                                               "<br/>Trigger = " + str(alarmTriggered) +
                                               "<br/>Timer = " + str(alarmTimeout) +
                                               "<br/>Contacts = " + str(alarmStatus) +
                                               "<br/>Move = " + str(moveStatus))
                            elif "presence" == urlTokens[3]:
                                if 4 < urlTokensLen:
                                    if "enable" == urlTokens[4]:
                                        presenceIsEnabled = True
                                        self.ok200("Presence is enabled")
                                    elif "disable" == urlTokens[4]:
                                        presenceIsEnabled = False
                                        self.ok200("Presence is disabled")
                                    else:
                                        self.ok200("Presence is enabled = " + str(presenceIsEnabled))
                                else:
                                    self.ok200("Presence is enabled = " + str(presenceIsEnabled))
                            elif "move" == urlTokens[3]:
                                if 4 < urlTokensLen:
                                    if "enable" == urlTokens[4]:
                                        moveIsEnabled = True
                                        self.ok200("Move is enabled")
                                    elif "disable" == urlTokens[4]:
                                        moveIsEnabled = False
                                        self.ok200("Move is disabled")
                                    else:
                                        self.ok200("Move is enabled = " + str(moveIsEnabled) + "<br/>" + "Move = " + str(moveStatus))
                                else:
                                    self.ok200("Move is enabled = " + str(moveIsEnabled) + "<br/>" + "Move = " + str(moveStatus))
                            elif "node" == urlTokens[3]:
                                self.ok200(str(nodeList))
                            elif "sendsms" == urlTokens[3]:
                                if 4 < urlTokensLen:
                                    self.ok200("Sending SMS: " + urlTokens[4])
                                    sendSMS(urlTokens[4])
                            else:
                                self.error404("Bad command for node " + node + ": " + urlTokens[3])
                        else:
                            self.error404("No command for node: " + node)
                    else:
                        self.error404("Bad node: " + node)
                else:
                    self.error404("Command too short: " + api)
            else:
                self.error404("Bad location: " + api)
        else:
            self.error404("Url too short")


serial2http = Serial2Http("Serial2Http")
http2serial = http.server.HTTPServer(("", HTTPD_PORT), CustomHandler)


def signal_term_handler(signal_, frame_):
    log('Got SIGTERM, exiting...')
    global http2serial
    http2serial.server_close()
    global serial2http
    serial2http.stop()
    time.sleep(2.0)
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_term_handler)
    serial2http.start()
    log("Serving at port " + str(HTTPD_PORT))
    try:
        http2serial.serve_forever()
    except KeyboardInterrupt:
        serial2http.stop()
        pass
    log("Stopping HTTP server")
    http2serial.server_close()

#! /usr/bin/env python3
# coding: utf-8

import http.server
import threading
import time
import requests
import serial

nodeList = dict(
    dining={'port': '/dev/dining', 'fd': serial.Serial(), 'errorCnt': 0},
    kitchen={'port': '/dev/kitchen', 'fd': serial.Serial(), 'errorCnt': 0},
    bedroom={'port': '/dev/bedroom', 'fd': serial.Serial(), 'errorCnt': 0})

SERIALLOOPNB = 0

for nodeSerial in nodeList:
    nodeList[nodeSerial]['fd'].port = nodeList[nodeSerial]['port']
    nodeList[nodeSerial]['fd'].baudrate = 115200
    nodeList[nodeSerial]['fd'].parity = serial.PARITY_NONE
    nodeList[nodeSerial]['fd'].stopbits = serial.STOPBITS_ONE
    nodeList[nodeSerial]['fd'].bytesize = serial.EIGHTBITS
    nodeList[nodeSerial]['fd'].timeout = 0.1

MAX_NODE_ERRORS = 10
HTTPD_PORT = 8444
OLIVIER_PHONE = "0689350159"
OLIVIER_EMAIL = "cambon.olivier@gmail.com"

jeedomUrl = {'dining ping get': '',
             'dining windowShutterButton hk 0': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=192',
             'dining windowShutterButton hk 1': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=190',
             'dining windowShutterButton hk 2': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=191',
             'dining windowWindowContact hk 1': '',
             'dining windowWindowContact hk 0': '',
             'dining windowShutterContact hk 1': '',
             'dining windowShutterContact hk 0': '',
             'dining doorWindowContact hk 1': '',
             'dining doorWindowContact hk 0': '',
             'dining doorShutterContact hk 1': '',
             'dining doorShutterContact hk 0': '',
             'dining tvWindowContact hk 1': '',
             'dining tvWindowContact hk 0': '',
             'dining tvShutterContact hk 1': '',
             'dining tvShutterContact hk 0': '',
             'dining lightRelay get 1': '',
             'dining lightRelay get 0': '',
             'kitchen ping get': '',
             'kitchen windowWindowContact hk 1': '',
             'kitchen windowWindowContact hk 0': '',
             'kitchen windowShutterContact hk 1': '',
             'kitchen windowShutterContact hk 0': '',
             'kitchen doorShutterButton hk 0': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=202',
             'kitchen doorShutterButton hk 1': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=200',
             'kitchen doorShutterButton hk 2': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=201',
             'kitchen doorWindowContact hk 1': '',
             'kitchen doorWindowContact hk 0': '',
             'kitchen doorShutterContact hk 1': '',
             'kitchen doorShutterContact hk 0': '',
             'kitchen lightRelay get 1': '',
             'kitchen lightRelay get 0': '',
             'bedroom ping get': '',
             'bedroom parentsShutterButton hk 0': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=167',
             'bedroom parentsShutterButton hk 1': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=165',
             'bedroom parentsShutterButton hk 2': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=166',
             'bedroom parentsWindowContact hk 1': '',
             'bedroom parentsWindowContact hk 0': '',
             'bedroom parentsShutterContact hk 1': '',
             'bedroom parentsShutterContact hk 0': '',
             'bedroom ellisShutterButton hk 0': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=162',
             'bedroom ellisShutterButton hk 1': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=160',
             'bedroom ellisShutterButton hk 2': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=161',
             'bedroom ellisWindowContact hk 1': '',
             'bedroom ellisWindowContact hk 0': '',
             'bedroom ellisShutterContact hk 1': '',
             'bedroom ellisShutterContact hk 0': '',
             'bedroom desktopShutterButton hk 0': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=172',
             'bedroom desktopShutterButton hk 1': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=170',
             'bedroom desktopShutterButton hk 2': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=171',
             'bedroom desktopWindowContact hk 1': '',
             'bedroom desktopWindowContact hk 0': '',
             'bedroom desktopShutterContact hk 1': '',
             'bedroom desktopShutterContact hk 0': '',
             'bedroom lightRelay get 1': '',
             'bedroom lightRelay get 0': '',
             }


# Ajouter:
# - ping avec timeout puis sendSMS
# - try/catch sur requests.get avec retry puis sendSMS
# - jeedomURL bedroom
# - tester toutes les contacts window et shutter
# - tester le shutterButton sur bedroom

def httpRequest(url):
    requests.get(url)


def sendSMS(tel, msg):
    pass


def sendEmail(email, object, msg):
    pass


def sendAlert(msg):
    sendSMS(OLIVIER_PHONE, msg)
    sendEmail(OLIVIER_EMAIL, "Alerte", msg)


def error(node, e):
    if MAX_NODE_ERRORS > nodeList[node]['errorCnt']:
        nodeList[node]['errorCnt'] += 1
    if MAX_NODE_ERRORS == nodeList[node]['errorCnt']:
        sendAlert(node + " " + e)
        nodeList[node]['errorCnt'] += 1


class Serial2Http(threading.Thread):
    def run(self):
        while True:
            for node in nodeList:
                try:
                    if nodeList[node]['fd'].isOpen() is False:
                        print("Opening " + nodeList[node]['fd'].port)
                        # print(nodeList[node]['fd'].get_settings())
                        nodeList[node]['fd'].open()
                        nodeList[node]['fd'].flushInput()
                    if nodeList[node]['fd'].isOpen() is True:
                        if 0 < nodeList[node]['fd'].inWaiting():
                            line = nodeList[node]['fd'].readline().decode("utf-8").rstrip()
                            if "" != line:
                                if line in jeedomUrl:
                                    if "" != jeedomUrl[line]:
                                        print("Serial CMD=" + line)
                                        requests.get(jeedomUrl[line])
                                        nodeList[node]['errorCnt'] = 0
                                else:
                                    print("ERROR: Serial CMD '" + line + "' not found !")
                        #if 0 == SERIALLOOPNB % 100:
                        #    nodeList[node]['fd'].write(("\n\n" + node + " ping get\n\n").encode('utf-8'))
                except Exception as e:
                    print("ERROR Exception: " + str(e))
                    nodeList[node]['fd'].close()
                    error(node, str(e))
                    time.sleep(1.0)
            time.sleep(0.01)
            #SERIALLOOPNB += 1


class CustomHandler(http.server.BaseHTTPRequestHandler):
    def ok200(self, resp: str):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(resp.encode())

    def error404(self, resp: str):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(resp.encode())

    def do_GET(self):
        urlTokens = self.path.split('/')
        urlTokensLen = len(urlTokens)
        print(urlTokens)
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
                            self.ok200(cmd)
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


if __name__ == '__main__':
    serial2http = Serial2Http(name="Serial2Http")
    serial2http.start()
    httpd = http.server.HTTPServer(("", HTTPD_PORT), CustomHandler)

    print("Serving at port ", HTTPD_PORT)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print("Stopping HTTP server")
    httpd.server_close()

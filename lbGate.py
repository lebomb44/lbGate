#! /usr/bin/env python3
# coding: utf-8

import http.server
import threading
import time
import requests
import serial
from typing import Dict, Union

nodeList: Dict[str, Dict[str, Union[str, serial.Serial]]] = dict(
	kitchen={'port': '/dev/ttyUSB0', 'fd': serial.Serial()})

for node in nodeList:
	nodeList[node]['fd'].port = nodeList[node]['port']
	nodeList[node]['fd'].baudrate = 115200
	nodeList[node]['fd'].parity = serial.PARITY_NONE
	nodeList[node]['fd'].stopbits = serial.STOPBITS_ONE
	nodeList[node]['fd'].bytesize = serial.EIGHTBITS
	nodeList[node]['fd'].timeout = 0.1

HTTPD_PORT = 8444

jeedomUrl = {'kitchen_doorShutter 0': 'http://sno.ddns.net/jeedom/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=202',
			 'kitchen_doorShutter 1': 'http://sno.ddns.net/jeedom/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=200',
			 'kitchen_doorShutter 2': 'http://sno.ddns.net/jeedom/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=201',
			 'cmd4': 'http://localhost/jeedom/test',
			 'cmd5': 'http://localhost/jeedom/test'
			 }


class Serial2Http(threading.Thread):
	def run(self):
		while True:
			for node in nodeList:
				if nodeList[node]['fd'].is_open is False:
					print("Opening " + nodeList[node]['fd'].port)
					print(nodeList[node]['fd'].get_settings())
					nodeList[node]['fd'].open()
				if nodeList[node]['fd'].is_open is True:
					line: str = nodeList[node]['fd'].readline().decode("utf-8").rstrip()
					if "" != line:
						print("Serial CMD=" + line)
						if line in jeedomUrl:
							requests.get(jeedomUrl[line])
						else:
							print("ERROR: Serial CMD '" + line + "' not found !")
			time.sleep(0.01)


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
		urlTokensLen: int = len(urlTokens)
		print(urlTokens)
		if 1 < urlTokensLen:
			api: str = urlTokens[1]
			if "api" == api:
				if 2 < urlTokensLen:
					node: str = urlTokens[2]
					if node in nodeList:
						if 3 < urlTokensLen:
							cmd: str = node + "_" + urlTokens[3]
							if 4 < urlTokensLen:
								for token in urlTokens[4:]:
									cmd = cmd + " " + token
							nodeList[node]['fd'].write(cmd)
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

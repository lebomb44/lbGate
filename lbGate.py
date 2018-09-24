#! /usr/bin/env python3
# coding: utf-8

import http.server
import threading
import time
import requests
import serial

nodeList = dict(
	kitchen={'port': '/dev/ttyUSB1', 'fd': serial.Serial()})

for node in nodeList:
	nodeList[node]['fd'].port = nodeList[node]['port']
	nodeList[node]['fd'].baudrate = 115200
	nodeList[node]['fd'].parity = serial.PARITY_NONE
	nodeList[node]['fd'].stopbits = serial.STOPBITS_ONE
	nodeList[node]['fd'].bytesize = serial.EIGHTBITS
	nodeList[node]['fd'].timeout = 0

HTTPD_PORT = 8444

jeedomUrl = {'kitchen_doorShutterButton_hk 0': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=202',
			 'kitchen_doorShutterButton_hk 1': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=200',
			 'kitchen_doorShutterButton_hk 2': 'http://localhost/core/api/jeeApi.php?apikey=nAx7bK300sR01CCq20mXJbsYaYcWc84hfPEY3W1Rnh27BTDb&type=cmd&id=201',
			 'cmd4': 'http://localhost/jeedom/test',
			 'cmd5': 'http://localhost/jeedom/test'
			 }


class Serial2Http(threading.Thread):
	def run(self):
		while True:
			for node in nodeList:
				if nodeList[node]['fd'].isOpen() is False:
					print("Opening " + nodeList[node]['fd'].port)
					#print(nodeList[node]['fd'].get_settings())
					nodeList[node]['fd'].open()
					nodeList[node]['fd'].flushInput()
				if nodeList[node]['fd'].isOpen() is True:
					if 0 < nodeList[node]['fd'].inWaiting():
						line = nodeList[node]['fd'].readline().decode("utf-8").rstrip()
						if "" != line:
							if line in jeedomUrl:
								print("Serial CMD=" + line)
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
		urlTokensLen = len(urlTokens)
		print(urlTokens)
		if 1 < urlTokensLen:
			api = urlTokens[1]
			if "api" == api:
				if 2 < urlTokensLen:
					node = urlTokens[2]
					if node in nodeList:
						if 3 < urlTokensLen:
							cmd = node + "_" + urlTokens[3]
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

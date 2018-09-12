#! /usr/bin/env python3
# coding: utf-8

import sys, os, re, shutil, json, urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
import lbSerial

HTTPD_PORT = 8444

class CustomHandler(BaseHTTPRequestHandler):
	def ok200(self, resp):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write(resp.encode())
	def error404(self, resp):
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
					if True == lbSerial.isAccepted(node):
						cmd = ""
						for token in urlTokens:
							cmd = cmd + " " + token
						lbSerial.send(cmd)
						self.ok200(cmd)
					else:
						self.error404("Bad node: " + node)
				else:
					self.error404("Command to short: " + api)
			else:
				self.error404("Bad location: " + api)
		else:
			self.error404("Url too short")

if __name__=='__main__':
	httpd = HTTPServer(("", HTTPD_PORT), CustomHandler)

	print("Serving at port ", HTTPD_PORT)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	print("Stopping HTTP server")
	httpd.server_close()


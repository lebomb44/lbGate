#! /usr/bin/env python3
# coding: utf-8

import lbSerial
import serial

nodeList = { 'kitchen': { 'port': '/dev/ttyS0', 'fd': serial.Serial() }, \
		'dining' : { 'port': '/dev/ttyS1', 'fd': serial.Serial() }, \
		'bedroom': { 'port': '/dev/ttyS2', 'fd': serial.Serial() }, \
		'ext'    : { 'port': '/dev/ttyS3', 'fd': serial.Serial() }, \
		'safety' : { 'port': '/dev/ttyS4', 'fd': serial.Serial() }, \
		}

for node in nodeList:
	nodeList[node]['fd'].port=nodeList[node]['port']
	nodeList[node]['fd'].parity=serial.PARITY_NONE
	nodeList[node]['fd'].stopbits=serial.STOPBITS_ONE
	nodeList[node]['fd'].bytesize=serial.EIGHTBITS
	nodeList[node]['fd'].timeout=1

def isAccepted(node):
	try:
		_node = nodeList[node]
		return True
	except KeyError:
		return False

def send(node, cmd):
	if False == nodeList[node]['fd'].is_open:
		nodeList[node]['fd'].open()
	if True == nodeList[node]['fd'].is_open:
		print(cmd)


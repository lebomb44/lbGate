#!/usr/bin/python

import sys, getopt
import datetime
import serial

def main(argv):
	serport = '/dev/ttyS0'
	inputfile = ''
	outputfile = str(datetime.datetime.utcnow()) + '_cmdBatch.log'
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'cmdBatch.py -i <inputfile> -o <outputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'cmdBatch.py -i <inputfile> -o <outputfile>'
			sys.exit()
		elif opt in ("-p", "--port"):
			port = arg
		elif opt in ("-i", "--ifile"):
			inputfile = arg
	print 'Command file used: ', inputfile
	print 'Output file used: ', outputfile

	ser = serial.Serial(port=serport, baudrate=500000, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
	inputfd = open(inputfile, "r")
	outputfd = open(outputfile, "w")
	nbInputCmd = 0
	nbOutputCmd = 0
	for inputcmd in inputfd:
		ser.write(inputcmd)
		outputfd.write(inputcmd)
		sys.stdout.write(inputcmd)
		nbInputCmd += 1
		outputcmd = ser.readline()
		outputfd.write(outputcmd)
		sys.stdout.write(outputcmd)
		nbOutputCmd +=1
	ser.close()
	inputfd.close()
	outputfd.close()
	
	print "Commands sent to SOCAN EGSE: " + str(nbInputCmd)
	print "Answers received from SOCAN EGSE: " + str(nbOutputCmd)

if __name__ == "__main__":
   main(sys.argv[1:])


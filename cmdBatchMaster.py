#!/usr/bin/python

import sys, getopt
import datetime
import serial
import time

def main(argv):

#	definition des variables	
	nbInputCmd = 0
	nbOutputCmd = 0

#------------------------- SOCAN EGSE SPY -------------------------
#	port serie pour le Spy	
	serportSpy = '/dev/ttyACM0'
	inputfileSpy = 'CommandeSpy.txt'
	outputfileSpy = str(datetime.datetime.utcnow()) + '_cmdBatchSpy.log'
	try:
		opts, args = getopt.getopt(argv,"h:ip",["portSpy=","ifileSpy="])
	except getopt.GetoptError:
		print 'cmdBatch.py -p <serialport> -i <inputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'cmdBatch.py -p <serialport> -i <inputfile>'
			sys.exit()
		elif opt in ("-p", "--port"):
			serportSpy = arg
		elif opt in ("-i", "--ifile"):
			inputfileSpy = arg
#	parametrage du port serie Spy	
	serSpy = serial.Serial(port=serportSpy, baudrate=500000, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.5)
#	ouverture des fichiers Spy
	inputfdSpy = open(inputfileSpy, "r")
	outputfdSpy = open(outputfileSpy, "w")
	time.sleep(3)
#	affichage du menu Spy
	for i in range(3):	
		outputcmdSpy = serSpy.readline()
		outputfdSpy.write(outputcmdSpy)
#	affichage de menu help
#	serSpy.write("help\n")	
#	outputfdSpy.write("help\n")
#	for i in range(25):	
#		outputcmdSpy = serSpy.readline()
#		outputfdSpy.write(outputcmdSpy)
#	pour chaque ligne du fichier commande Spy
	for inputcmdSpy in inputfdSpy:
		serSpy.write(inputcmdSpy)
		outputfdSpy.write(inputcmdSpy)
		outputcmdSpy = serSpy.readline()
		outputfdSpy.write(outputcmdSpy)



#------------------------- SOCAN EGSE MASTER -------------------------
#	port serie pour le Master
	serportMaster = '/dev/ttyACM1'
	inputfileMaster = 'CommandeMasterPL.txt'
	try:
		opts, args = getopt.getopt(argv,"h:ip",["port=","ifile="])
	except getopt.GetoptError:
		print 'cmdBatch.py -p <serialport> -i <inputfile>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'cmdBatch.py -p <serialport> -i <inputfile>'
			sys.exit()
		elif opt in ("-p", "--port"):
			serportMaster = arg
		elif opt in ("-i", "--ifile"):
			inputfileMaster = arg
#	parametrage du port serie Master	
	serMaster = serial.Serial(port=serportMaster, baudrate=500000, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.5)
	time.sleep(1.0)
#	ouverture des fichiers Master
	inputfdMaster = open(inputfileMaster, "r")
#	affichage du menu Master	
	for i in range(3):	
		outputcmdMaster = serMaster.readline()
		sys.stdout.write(outputcmdMaster)	
		time.sleep(0.5)
#	affichage de menu help
#	serMaster.write("help\n")	
#	sys.stdout.write("help\n")
#	for i in range(25):	
#		outputcmdMaster = serMaster.readline()
#		sys.stdout.write(outputcmdMaster)
#	pour chaque ligne du fichier commande Master
	for inputcmdMaster in inputfdMaster:		
		if "#" in str(inputcmdMaster):
			nbInputCmd += 1
		else:		
			serMaster.write(inputcmdMaster)
			sys.stdout.write(inputcmdMaster)	
			if "show" in str(inputcmdMaster):
				for i in range (30):
					outputcmdMaster = serMaster.readline()	
					sys.stdout.write(outputcmdMaster)
					if "DONE" in str(outputcmdMaster):
						nbInputCmd += 1
					elif "Bad" in str(outputcmdMaster):
						print "There is an error in the values used for the command.\n"
						sys.exit(0)
					elif "not" in str(outputcmdMaster):
						print "There is an error in the syntax command.\n"					
						sys.exit(0)
					elif "error" in str(outputcmdMaster):
						print "There is an error in the command.\n"					
						sys.exit(0)
					elif "REJECTED" in str(outputcmdMaster):
						print "The profile created contains one or more messages which are not created.\n"
						sys.exit(0)
					elif "ERR" in str(outputcmdMaster):
						print "The Msg or Profile sent is not created.\n"						
						sys.exit(0)
					elif "Syntax" in str(outputcmdMaster):
						print "The syntax used is wrong.\n"						
						sys.exit(0)

			elif "create" in str(inputcmdMaster):
				for i in range (3):		
					outputcmdMaster = serMaster.readline()	
					sys.stdout.write(outputcmdMaster)
					if "DONE" in str(outputcmdMaster):
						nbInputCmd +=1
					elif "Bad" in str(outputcmdMaster):
						print "There is an error in the values used for the command.\n"
						sys.exit(0)
					elif "not" in str(outputcmdMaster):
						print "There is an error in the syntax command.\n"					
						sys.exit(0)
					elif "error" in str(outputcmdMaster):
						print "There is an error in the command.\n"					
						sys.exit(0)
					elif "REJECTED" in str(outputcmdMaster):
						print "The profile created contains one or more messages which are not created.\n"
						sys.exit(0)
					elif "ERR" in str(outputcmdMaster):
						print "The Msg or Profile sent is not created.\n"						
						sys.exit(0)
					elif "Syntax" in str(outputcmdMaster):
						print "The syntax used is wrong.\n"						
						sys.exit(0)

			elif "sendPRO" in str(inputcmdMaster):		
				nbPROsent = str(inputcmdMaster)[8:]	#recherche du nb de profil envoyes
				nbPROsent = int(nbPROsent) * 24			
				for i in range (nbPROsent+1):	#lire et ecrire dans un fichier les reponses du Spy
					while True :
						a = serSpy.inWaiting()
						if a!=0: break				
					outputcmdSpy = serSpy.readline()	
					outputfdSpy.write(outputcmdSpy)
					sys.stdout.write(outputcmdSpy)
				nbInputCmd +=1

			elif "sendMSG" in str(inputcmdMaster):
				for i in range (2):	#lire et ecrire dans un fichier les reponses du Spy
					outputcmdSpy = serSpy.readline()	
					outputfdSpy.write(outputcmdSpy)
					sys.stdout.write(outputcmdSpy)
				nbInputCmd +=1
					
			nbOutputCmd += 1
			
	serMaster.close()
	inputfdMaster.close()
	serSpy.close()
	inputfdSpy.close()
	outputfdSpy.close()

if __name__ == "__main__":
   main(sys.argv[1:])


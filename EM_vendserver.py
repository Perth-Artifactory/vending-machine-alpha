#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import serial
import MySQLdb as mdb
import socket
import os
import os.path
import sys
import syslog
import MySQLdb
import io
import time

EM4='/dev/ttyUSB4'
CONTROL='/dev/ttyUSB0'
KEYPAD='/dev/ttyUSB3'
# TODO, Incluse Asking code for Arduinos so we dont need to specify the ports, Discover automagically

con = mdb.connect('localhost', 'vend', 'vend', 'vend');
mainmessage = "Welcome to The Artifactory, Please scan NFC or Tag to begin ...."
irker_server = ('core', 6659)
target = 'ircs://chat.freenode.net/artifactorys'
subsystem = 'Vendo: '
EM4reader = serial.Serial(EM4, 9600)


def connect():
    return socket.create_connection(irker_server)

def send(s, target, message):
    data = {"to": target, "privmsg" : message}
    dump = json.dumps(data)
    if not isinstance(dump, bytes):
        dump = dump.encode('ascii')
    s.sendall(dump)

def beginvend():
	cur.execute("SELECT balance FROM users WHERE cardid = %s",(data))
	row = cur.fetchone()
	if row :
		print row
		irk('EM4 Card Presented: ' +row[0])
		balance = "%s" % row

	# here is the big issue, The way the screen works is its expecting to see 64 Characters sent to it (Its also the way i programmed it)
	# but sending spaces seems to not work.. So i made it send hypens instead
	displaydata = ("python /home/pi/display.py  Welcome-User:------%s---Credit=%s--------- -----------"%(data,balance))
	os.system(displaydata)
	os.system('python /home/pi/display.py  Please-Select---1:DONATION------2:TOP-UP--------3:VENDING-------- -')
	looper = True
	readkeypad()
def readkeypad():
	VENDkeypad = serial.Serial(KEYPAD, 9600)
	# flush the toilet.. line..
	VENDkeypad.flushInput()
	VENDkeypad.flushOutput()
	keydata = VENDkeypad.readline().strip()
	while True:
		if keydata:
			True
			print (keydata)
			if "1" in keydata:
				# We should use a Case here, Switch.
				print("Hey It works") # Debug stuff
				os.system("python /home/pi/display.py  --------------------DONATION------------------------------------- -")
				os.system("python /home/pi/display.py  ------------------Please-Insert--------Donation------------------ -")
				#something here to drive the coin acceptor, TODO
				time.sleep(5)
				# Hack to clear what is in the buffer of the serial port, Incase a button is accidentally pressed
				keydata = ''

			if "2" in keydata:
				os.system("python /home/pi/display.py  -----------------TOP-UP-CREDIT----------------------------------- -")
				os.system("python /home/pi/display.py  Please-Insert---Coins-----------When-Done-Press----STAR---------- -")
				#something here to drive the coin acceptor, TODO
				time.sleep(5)
				keydata = ''

			if "3" in keydata:
				os.system("python /home/pi/display.py  --Select-Slot--------------------------------------------------- -")
				VENDkeypad.flushInput()
				VENDkeypad.flushOutput()
				keydata = VENDkeypad.readline().strip()
				if "1" in keydata:
					os.system("python /home/pi/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/pi/dispenser.py A")
					time.sleep(5)
					return


				if "2" in keydata:
					os.system("python /home/pi/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/pi/dispenser.py B")
					time.sleep(5)
					return


				if "3" in keydata:
					os.system("python /home/pi/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/pi/dispenser.py C")
					time.sleep(5)
					return


				if "4" in keydata:
					os.system("python /home/pi/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/pi/dispenser.py D")
					time.sleep(5)
					return

				if "5" in keydata:
					os.system("python /home/pi/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/pi/dispenser.py E")
					time.sleep(5)
					return

				if "6" in keydata:
					os.system("python /home/pi/display.py  --Dispensing---------------------------------------------------- -")

					os.system("python /home/pi/dispenser.py F")
					time.sleep(5)
					return

				if "7" in keydata:
					os.system("python /home/pi/display.py  --Dispensing---------------------------------------------------- -")

					os.system("python /home/pi/dispenser.py G")
					time.sleep(5)
					return

				if "8" in keydata:
					os.system("python /home/pi/display.py  --Dispensing---------------------------------------------------- -")

					os.system("python /home/pi/dispenser.py H")
					time.sleep(5)
					return

				if "9" in keydata:
					os.system("python /home/pi/display.py  --Dispensing---------------------------------------------------- -")

					os.system("python /home/pi/dispenser.py I")
					time.sleep(5)
					return

				if "*" in keydata:
					return


				VENDkeypad.flushInput()
				VENDkeypad.flushOutput()
				keydata = ''

				# well at the moment we can read 0-9 but not 2 characters... so really only 10 slots work.. Need to work on this.

				time.sleep(5)
			else:
				return()



def enroll():
	# DO NOT LOOK, BAD CODE... But it works... MK
	displaydata = ("python /home/pi/display.py  Card-Not-Found--Card-Enrolled---ID:%s------------------- -"%(data))
	os.system(displaydata)

	print "Enrolling card ID: "
	print(data)
	cur = con.cursor()
	cur.execute('INSERT into users (cardid, balance, cardtype) values (%s, %s, %s)',(data, '00000', 'EM4'))
	con.commit()
	print "Card Enrolled, GO back to main thing"

	return


def irk(message):
    try:
        s = connect()
        send(s, target, subsystem + message)
        s.close()
    except socket.error as e:
        sys.stderr.write("irk: write to server failed: %r\n" % e)


# Stuff below here executed on startup
# ok so this is the main, I should probably put this in its own def.
while True:
	try:
		print "Opening EM4",EM4
		irk("EM4_vendserver.py Running")
		syslog.syslog("VENDO: Checking for EM4 Reader")
 		if os.path.isfile(EM4) and os.access(EM4, os.R_OK):
			syslog.syslog("EM4 MISSING")
		else:
			syslog.syslog(" EM4 FOUND")
  			syslog.syslog(" Checking for Motor Control")
 		if os.path.isfile(CONTROL) and os.access(CONTROL, os.R_OK):
   			syslog.syslog(" Control MISSING")
 		else:
   			syslog.syslog(" Control FOUND")
 			syslog.syslog("VENDO: Ready!")
			print("Sending Display Data")
			# This one works below... Spaces dont work... so i used dashes... Why dont they work?
			os.system('python /home/pi/display.py  -----Welcome----Please-Scan-CardArtifactory-Vend-CodeBase-V01-- -')

		print('Main LOOP Running...')
		data = EM4reader.read(11).strip()
		if data:
			code = ''
			cur = con.cursor()
			
			# check if the card is in the database
			print "Checking if card is in database"
		      	print(data)
			cur.execute("SELECT * FROM users WHERE cardid = %s",(data))
			row = cur.fetchall()
			if row :
				print row
				# commented out for now to not spam
				#irk('EM4 Card Presented: ' +row[0])
				#irk('EM4 Card Owner: ' +row[3])
				#irk('EM4 Card Balance (Cents): ' +row[1])
				print 'Card Exists, Go to a new routine to start vending This part is done'
				beginvend()

				EM4reader.flushInput()
				EM4reader.flushOutput()
  			else:
	 			print 'Card does not exist, Go to the enroll routine.'
				EM4reader.flushInput()
				EM4reader.flushOutput()
				enroll()




				#enroll()
	

# Probably not right, I suck at python.. MK
	except MySQLdb.Error, e:
		try:
			print "It was a SQLError"
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		except IndexError:
			print "It was a IndexError"
            		print "MySQL Error: %s" % str(e)
		except TypeError, e:
			print "It was a TypeError"
        		print(e)
		except ValueError, e:
			print "It was a ValueError"
        		print(e)

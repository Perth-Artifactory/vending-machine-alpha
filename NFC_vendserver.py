#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
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

#NFC='/dev/ttyUSB4' # Usually this, pl2303 device
NFC='/dev/ttyUSB2' # Usually this, pl2303 device
KEYPAD='/dev/ttyUSB3' # changes
# TODO, Incluse Asking code for Arduinos so we dont need to specify the ports, Discover automagically

con = mdb.connect('localhost', 'vend', 'vend', 'vend');
mainmessage = "Welcome to The Artifactory, Please scan NFC or Tag to begin ...."
irker_server = ('core', 6659)
target = 'ircs://chat.freenode.net/artifactorys'
subsystem = 'Vendo: '
NFCreader = serial.Serial(NFC, 9600)

def takemoney():
	print "Reading How much the slot was: "
	cur.execute("SELECT price FROM prices WHERE slot = %s",(keydata))
	row = cur.fetchone()
	print "Slot Price: "
	price = row
	print"Taking money off card"
	cur.execute("SELECT balance FROM users WHERE cardid = %s",(data))
	row = cur.fetchone()
	print "Current Balance: "
	balance = row
	print "Slot Price: "
	print price
	price = price[0]
	balance = balance[0]
	print "Lets see if the two converted"
	print price
	print "And Balance"
	print balance
	newprice = int(price)
	newbalance = int(balance)
	currbalance = newbalance - newprice
	#newbalance = price - balance
	print "New Balance: "
	print currbalance
 	cur.execute("UPDATE users SET balance = %s WHERE cardid = %s",(currbalance,data))
	con.commit()

def subtract(price, balance):
    return price - balance

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
		irk('NFC Card Presented: ' +row[0])
		balance = "%s" % row

	# here is the big issue, The way the screen works is its expecting to see 64 Characters sent to it (Its also the way i programmed it)
	# but sending spaces seems to not work.. So i made it send hypens instead
	#os.system("python /home/mitch/display.py  Welcome-User:------%s---Credit=%s-------------------"%(data,balance))
	#					    ----Welcome-----Please-Scan-CardArtifactory-Vend-----Code-V9---
	#os.system("python /home/mitch/display.py       ----Welcome-----Please-Scan-CardArtifactory-Vend-----Code-V1-- -")

	os.system('python /home/mitch/display.py  Please-Select---1:DONATION------2:TOP-UP--------3:VENDING------')
	looper = True
	readkeypad()


def readkeypad():
	VENDkeypad = serial.Serial(KEYPAD, 9600)
	# flush the toilet.. line..
	VENDkeypad.flushInput()
	VENDkeypad.flushOutput()
	keydata = VENDkeypad.read(1).strip()
	print keydata
	while True:
		if keydata == 1 or 2 or 3:
			True
			print (keydata)
			if "1" in keydata:
				# We should use a Case here, Switch.
				print("Hey It works") # Debug stuff
				os.system("python /home/mitch/display.py  --------------------DONATION-----------------------------------")

				os.system("python /home/mitch/display.py  ------------------Please-Insert--------Donation----------------")

				#something here to drive the coin acceptor, TODO
				time.sleep(5)
				# Hack to clear what is in the buffer of the serial port, Incase a button is accidentally pressed
				keydata = ''

			if "2" in keydata:
				os.system("python /home/mitch/display.py  -----------------TOP-UP-CREDIT---------------------------------")

				os.system("python /home/mitch/display.py  Please-Insert---Coins-----------When-Done-Press----STAR--------")

				#something here to drive the coin acceptor, TODO
				time.sleep(5)
				keydata = ''

			if "3" in keydata:

				cur.execute("SELECT balance FROM users WHERE cardid = %s",(data))
				row = cur.fetchone()
				print "Checking not a negative: "
				balance = row
				balance = balance[0]
				print balance
				newbalance = int(balance)
				cur.execute("SELECT allowedzero FROM users WHERE cardid = %s",(data))
				row = cur.fetchone()
				print "Checking if allowed to go below 0: "
				allowed = balance[0]
				print allowed
				allowedzero = int(allowed)
				if allowedzero == 1:
					os.system("python /home/mitch/display.py  --Select-Slot--------------------------------------------------")

					VENDkeypad.flushInput()
					VENDkeypad.flushOutput()
					global keydata
					keydata = VENDkeypad.readline().strip()
				else:
					print "Balance not enough"
					os.system("python /home/mitch/display.py  --Insufficient-------Credit------------------------------------")
					time.sleep(2)
					return

				if keydata == "1":

					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------")
					os.system("python /home/mitch/dispenser.py A")
					takemoney()
					return


				if keydata == "2":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py B")
					keydata = keydata
					takemoney()
					return

				if keydata == "3":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py C")
					keydata = keydata
					takemoney()
					return

				if keydata == "3":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py D")
					keydata = keydata
					takemoney()
					return

				if keydata == "5":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py E")
					keydata = keydata
					takemoney()
					return

				if keydata == "6":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py F")
					keydata = keydata
					takemoney()
					return

				if keydata == "7":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py G")
					keydata = keydata
					takemoney()
					return

				if keydata == "8":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py H")
					keydata = keydata
					takemoney()
					return

				if keydata == "9":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py I")
					keydata = keydata
					takemoney()
					return

				if keydata == "10":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py J")
					keydata = keydata
					takemoney()
					return

				if keydata == "11":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py K")
					keydata = keydata
					takemoney()
					return

				if keydata == "12":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py L")
					keydata = keydata
					takemoney()
					return

				if keydata == "13":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py M")
					keydata = keydata
					takemoney()
					return

				if keydata == "14":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py N")
					keydata = keydata
					takemoney()
					return
				if keydata == "15":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py O")
					keydata = keydata
					takemoney()
					return
				if keydata == "16":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py P")
					keydata = keydata
					takemoney()
					return
				if keydata == "17":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py Q")
					keydata = keydata
					takemoney()
					return
				if keydata == "18":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py R")
					keydata = keydata
					takemoney()
					return
				if keydata == "19":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py S")
					keydata = keydata
					takemoney()
					return
				if keydata == "20":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py T")
					keydata = keydata
					takemoney()
					return
				if keydata == "21":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py U")
					keydata = keydata
					takemoney()
					return
				if keydata == "22":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py V")
					keydata = keydata
					takemoney()
					return
				if keydata == "23":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py W")
					keydata = keydata
					takemoney()
					return
				if keydata == "24":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py X")
					keydata = keydata
					takemoney()
					return
				if keydata == "25":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py Y")
					keydata = keydata
					takemoney()
					return
				if keydata == "26":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py Z")
					keydata = keydata
					takemoney()
					return
				if keydata == "27":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py a")
					keydata = keydata
					takemoney()
					return
				if keydata == "28":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py b")
					keydata = keydata
					takemoney()
					return
				if keydata == "29":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py c")
					keydata = keydata
					takemoney()
					return
				if keydata == "30":
					os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")
					os.system("python /home/mitch/dispenser.py d")
					keydata = keydata
					takemoney()
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
	os.system("python /home/mitch/display.py Card-Not-Found--Card-Enrolled----------------------------------")
	print "Enrolling card ID: "
	print(data)
	cur = con.cursor()
	cur.execute('INSERT into users (cardid, balance, cardtype) values (%s, %s, %s)',(data, '0000', 'NFC'))
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
		print "Opening NFC",NFC
		irk("NFC_vendserver.py Running")
		syslog.syslog("VENDO: Checking for NFC Reader")
 		if os.path.isfile(NFC) and os.access(NFC, os.R_OK):
			syslog.syslog("NFC MISSING")
		else:
			syslog.syslog(" NFC FOUND")
 			syslog.syslog("VENDO: Ready!")
			print("Sending Display Data")
			# This one works below... Spaces dont work... so i used dashes... Why dont they work?
			#os.system('python /home/mitch/display.py  "   Test" "1234"')
#			os.system("python /home/mitch/display.py  --Dispensing---------------------------------------------------- -")

			#os.system("python /home/mitch/display.py  ----Welcome-----Please-Scan-CardArtifactory-Vend-----Code-V1---- -")
							      #----Welcome-----Please-Scan-CardArtifactory-Vend-----Code-V9---
			os.system("python /home/mitch/display.py ----Welcome-----Please-Scan-CardArtifactory-Vend-----Code-V2---")


		print('Main LOOP Running...')
		global data
#		VENDkeypad = serial.Serial(KEYPAD, 9600)
		global keydata
#		keydata = VENDkeypad.readline().strip()
		data = NFCreader.readline().strip()
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
				#irk('NFC Card Presented: ' +row[0])
				#irk('NFC Card Owner: ' +row[3])
				#irk('NFC Card Balance (Cents): ' +row[1])
				print 'Card Exists, Go to a new routine to start vending This part is done'
				beginvend()

				NFCreader.flushInput()
				NFCreader.flushOutput()
  			else:
	 			print 'Card does not exist, Go to the enroll routine.'
				NFCreader.flushInput()
				NFCreader.flushOutput()
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

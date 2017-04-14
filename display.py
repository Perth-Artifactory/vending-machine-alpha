#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import time
import sys

serial = serial.Serial("/dev/ttyACM0",9600)
#time.sleep(2)
serial.setDTR(True)
maindata = sys.argv[1]
serial.write(maindata)
serial.close()

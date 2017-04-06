#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import time
import sys
print 'Dispensing Slot:'
print sys.argv[1]

serial = serial.Serial("/dev/ttyUSB0",9600)
time.sleep(2)
slot = sys.argv[1]
serial.write(slot)
serial.close()

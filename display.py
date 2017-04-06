#!/usr/bin/python
# -*- coding: utf-8 -*-

import serial
import time
import sys

serial = serial.Serial("/dev/ttyUSB2",9600)
time.sleep(2)
maindata = sys.argv[1]
altdata1 = sys.argv[2]
serial.write(maindata)
serial.write(altdata1)
serial.close()

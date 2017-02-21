#!/usr/bin/env python
# -*- coding: utf-8 -*-

SENSOR_TYPE="pressuremat"
BtnPin = 22
PROBE_TIMER = 60 # Anzahl Sekunden, die ein Standwaert gesendet werden soll

# #######################################################

import RPi.GPIO as GPIO
import time
import requests
import sys
import logging # for the following line
import os
import math
import ssl
from datetime import datetime
import socket
# ECG library
import ecglib

# #######################################################

ARG_DISPLAY=0
for arg in sys.argv:
    if arg == "-display":
        ARG_DISPLAY=1

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.add_event_detect(BtnPin, GPIO.BOTH, callback=detect, bouncetime=200)

def Print(x):
    if x == 0:
        if ARG_DISPLAY == 1:
            print '    *************************'
            print '    *   Matte ausgeloest!   *'
            print '    *************************'
            Status(1)

def Status(sensordata):
	if ARG_DISPLAY == 1:
		print "Status=",sensordata
  		try:
            context = ssl._create_unverified_context()
            url = read_secret("json_push","url","/home/pi/ecg/")
#       	print 'URL=%s' % url

            import json
            import urllib2

            SENSOR_FQN = SENSOR_QUALIFIER + "." + SENSOR_TYPE
            data =
                'SENSOR_FQN': 1
            }

            req = urllib2.Request(url)
            req.add_header('Content-Type', 'application/json')

            response = urllib2.urlopen(req, json.dumps(data), context=context)
        except:
            pass

def detect(chn):
    Print(GPIO.input(BtnPin))

def destroy():
    GPIO.cleanup()                     # Release resource

SENSOR_QUALIFIER = get_hostname()
if SENSOR_QUALIFIER == "":
	SENSOR_QUALIFIER=get_secret("hostname","hostname","/home/pi/ecg/")

if ARG_DISPLAY == 1:
	print "DEMO: " + SENSOR_TYPE
	print ""
	print "GPIO 25 (Pin 22) -> Kontakt #1 Matte"
	print "GRND    (Pin 20) -> Kontakt #2 Matte"
	print ""
	print "Ausgabe:"

setup()
try:
  while True:
    True
    time.sleep(PROBE_TIMER)
    Status(0)

except KeyboardInterrupt:
  destroy()

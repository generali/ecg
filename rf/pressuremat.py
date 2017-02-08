#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import requests
import sys
import logging # for the following line
import os
import math
import ssl
from datetime import datetime



BtnPin = 22
PROBE_TIMER = 60 # Anzahl Sekunden, die ein Standwaert gesendet werden soll

# #######################################################


ARG_DISPLAY=0
for arg in sys.argv:
        if arg == "-display":
                ARG_DISPLAY=1


if ARG_DISPLAY == 1:
	print "DEMO: Pressure mat"
	print ""
	print "GPIO 25 (Pin 22) -> Kontakt #1 Matte"
	print "GRND    (Pin 20) -> Kontakt #2 Matte"
	print ""
	print "Ausgabe:"

def read_secret(secret_name, mysecret, secret_path="./", secret_suffix=".secret"):
	# #######################################################
	# Liest Parameter aus der angegebenen Datei (.secret). Ermittelt
	# die Variable, die ebenfalls angegebenist und liefert deren Wert
	# zurück
	# #######################################################
	secret_file="%s%s%s" % (secret_path, secret_name, secret_suffix)
	if ARG_DISPLAY == 1:
		print "secret file: %s" % (secret_file)
	try:
    		config = {}
    		execfile(secret_file, config)
	except:
		if ARG_DISPLAY == 1:
			print "Error import secret file..."
		pass
	return config[mysecret]

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
#       		print 'URL=%s' % url

        		import json
        		import urllib2

        		data = {
             			'ECG1.pressuremat': 1
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

setup()
try:
  while True:
    True
    time.sleep(PROBE_TIMER)
    Status(0)

except KeyboardInterrupt:
  destroy()


#!/usr/bin/env python
# -*- coding: utf-8 -*-


SENSOR_TYPE = "motion"
PIR_PIN_BCM = 27

# ##############################################

import RPi.GPIO as GPIO
import time
import math
import ssl
import time
import sys
from datetime import datetime
import socket
# ECG library
import ecglib

ARG_DISPLAY=0
for arg in sys.argv:
	if arg == "-display":
		ARG_DISPLAY=1
	if arg == "-fast":
		varWaitTime=5

def MOTION(PIR_PIN):
	if ARG_DISPLAY == 1:
		print time.strftime("%b %d %Y %H:%M:%S", time.gmtime())+ " - Motion Detected!"
	try:
		context = ssl._create_unverified_context()

		url = read_secret("json_push","url","/home/pi/ecg/")
#		print 'URL=%s' % url

		import json
		import urllib2

		SENSOR_FQN = SENSOR_QUALIFIER + "." + SENSOR_TYPE
		data = {
			SENSOR_FQN: 1
		}

		req = urllib2.Request(url)
		req.add_header('Content-Type', 'application/json')

		response = urllib2.urlopen(req, json.dumps(data), context=context)

		# sleep to prevent massive database updates
		sleep(5000)
	except:
		pass

if __name__ == '__main__':
	SENSOR_QUALIFIER = get_hostname()
	if SENSOR_QUALIFIER == "":
		SENSOR_QUALIFIER=get_secret("hostname","hostname","/home/pi/ecg/")

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PIR_PIN_BCM, GPIO.IN)
	if ARG_DISPLAY == 1:
		print "PIR Module Test (CTRL+C to exit)"
		print "DEMO: " + SENSOR_TYPE
		print ""
		print "GPIO 27 (Pin 13) -> Signal Motion"
		print "VCC     (Pin 4) -> Motion Sensor VCC"
		print "GRND    (Pin 6) -> Motion Sensor GRND"
		print ""
		print "Ausgabe:"

	try:
		GPIO.add_event_detect(PIR_PIN_BCM, GPIO.RISING, callback=MOTION)
		while 1:
			time.sleep(100)
	except KeyboardInterrupt:
		GPIO.cleanup()

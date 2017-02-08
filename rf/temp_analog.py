#!/usr/bin/env python
# -*- coding: utf-8 -*-

SENSOR_TYPE="analog_temp"
varWaitTime=10

# ##########################################################

import ADC0832
import time
import math
import ssl
import time
import sys
from datetime import datetime

# ##########################################################

ARG_DISPLAY=0
for arg in sys.argv:
	if arg == "-display":
		ARG_DISPLAY=1
	if arg == "-fast":
		varWaitTime=5

def get_hostname():
	 print "Checking hostname..."
	 if socket.gethostname().find('.')>=0:
		name=socket.gethostname()
	 else:
		name=socket.gethostbyaddr(socket.gethostname())[0]
	 return name

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

def init():
	ADC0832.setup()
	if ARG_DISPLAY == 1:
		print("")
		print "DEMO: " + SENSOR_TYPE
		print("")
		print("ADC")
		print("ADC		   RPI")
		print("---------------------------------------")
		print("Pin 1		-> Pin 11 (GPIO 17)")
		print("Pin 2		-> (+++Sensor+++)")
		print("Pin 3		-> (+++ ohne +++)")
		print("Pin 4		-> Pin 9  (GND)")
		print("Pin 5 (DI)	-> Pin 13 (GPIO 27)")
		print("Pin 6 (DO)	-> Pin 13 (GPIO 27)")
		print("Pin 7 (CLK)	-> Pin 12 (GPIO 18)")
		print("Pin 8 (VCC)	-> Pin 1  (3.3V)")
		print("")
		print("Sensor (beliebiger analoger Sensor")
		print("Sensor")
		print("---------------------------------------")
		print("Pin -		-> Pin 9  (GND)")
		print("Pin +		-> Pin 1  (3.3V)")
		print("Pin S		-> (+++Pin 2 ADC+++)")
		print("")

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

def loop():
	while True:
		analogVal = ADC0832.getResult()
#		print 'temp analog= %d C' % analogVal
		Vr = 5 * float(analogVal) / 255
		Rt = 10000 * Vr / (5 - Vr)
		temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
		temp = temp - 273.15
		temp = float("{0:.2f}".format(temp))

		t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		if ARG_DISPLAY == 1:
			print '%s Temperatur = %.2f C (Wartezeit: %ss)' % (t, temp, varWaitTime)

		try:
			context = ssl._create_unverified_context()

			url = read_secret("json_push","url","/home/pi/ecg/")
#			print 'URL=%s' % url

			import json
			import urllib2

            SENSOR_FQN = SENSOR_QUALIFIER + "." + SENSOR_TYPE
            data = {
			         SENSOR_FQN: 1
            }

			req = urllib2.Request(url)
			req.add_header('Content-Type', 'application/json')

			response = urllib2.urlopen(req, json.dumps(data), context=context)
		except:
			pass
		time.sleep(varWaitTime)

if __name__ == '__main__':
    SENSOR_QUALIFIER = get_hostname()
    if SENSOR_QUALIFIER == "":
	       SENSOR_QUALIFIER=get_secret("hostname","hostname","/home/pi/ecg/")

	init()
	try:
		loop()
	except KeyboardInterrupt:
		ADC0832.destroy()
		if ARG_DISPLAY == 1:
			print 'Done.'

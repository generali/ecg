#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# WARNING: never rename file to "bluetooth.py" or this script will fail because of the import
# command, which will try to implementi itself and report an "AttributeError"
#

bt = ['CC:20:E8:64:0A:7F', '34:4D:AA:AD:7F:C0']
# You can hardcode the desired device ID here as a string to skip the discovery stage
addr = "CC:20:E8:64:0A:7F"
varWaitTime = 30

SENSOR_TYPE="bluetooth"

# #################################################

import bluetooth
import time
import sys
import requests
import ssl
import socket

# #################################################

ARG_DISPLAY=0
ARG_DEBUG=0
for arg in sys.argv:
	if arg == "-display":
		ARG_DISPLAY=1
	if arg == "-debug":
		ARG_DEBUG=1
	if arg == "-fast":
		varWaitTime=5

def get_hostname():
	if ARG_DISPLAY == 1:
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
	# default value
	#config[mysecret]="ERROR"
	if ARG_DISPLAY == 1:
		print "INFO: secret file: %s" % (secret_file)
	try:
		config = {}
		execfile(secret_file, config)
		if ARG_DISPLAY == 1:
			print "INFO: %s=%s" % (mysecret,config[mysecret])
	except:
		#if ARG_DISPLAY == 1:
		print "ERROR: Error import secret file... (missing secret file?)"
		pass
	return config[mysecret]

def UpdateStatus(status):
  try:
		context = ssl._create_unverified_context()

		url = read_secret("json_push","url","/home/pi/ecg/")
#       print 'URL=%s' % url

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

# ##################################

SENSOR_QUALIFIER = get_hostname()
if SENSOR_QUALIFIER == "":
	SENSOR_QUALIFIER=get_secret("hostname","hostname","/home/pi/ecg/")

if ARG_DISPLAY == 1:
	print "DEMO: " + SENSOR_TYPE
	print ("#" * 40)
	print "Hostname: " + SENSOR_QUALIFIER
	print "Searching for " + addr
	print "Ausgabe:"

while True:
	# Try to gather information from the desired device.
	# We're using two different metrics (readable name and data services)
	# to reduce false negatives.
	state = bluetooth.lookup_name(addr, timeout=20)
	services = bluetooth.find_service(address=addr)
	# Flip the LED pin on or off depending on whether the device is nearby
	if state == None and services == []:
		if ARG_DISPLAY == 1:
			print("No device detected in range...")
	else:
		if ARG_DISPLAY == 1:
			print("Device detected!")
		UpdateStatus(1)
	# Arbitrary wait time
	time.sleep(varWaitTime)

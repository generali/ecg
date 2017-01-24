#!/usr/bin/env python

import bluetooth
import time
import sys

bt = ['CC:20:E8:64:0A:7F', '34:4D:AA:AD:7F:C0']
varWaitTime = 30


ARG_DISPLAY=0
for arg in sys.argv:
        if arg == "-display":
                ARG_DISPLAY=1


if ARG_DISPLAY == 1:
	print "DEMO: Bluetooth Tag"
	print ""
	print "Ausgabe:"


def UpdateStatus():
  try:
     	context = ssl._create_unverified_context()

     	url = open('/home/pi/circonus/ecg1_sensors_url.txt', 'r').read()
#    	print 'URL=%s' % url

     	import json
     	import urllib2

     	data = {
             'ECG1.bluetooth': 1
     	}

     	req = urllib2.Request(url)
	req.add_header('Content-Type', 'application/json')

  	response = urllib2.urlopen(req, json.dumps(data), context=context)
  except:
	pass
			
			
			
			
try:
  while True:
    for i in range (len(bt)):
      doublecheck = 0
      while doublecheck < 1:
	print("Scanning device: %s" % bt[i])
        result = bluetooth.lookup_name(bt[i], timeout=3)
        if (result != None):
          # bluetooth device in range
          if ARG_DISPLAY == 1:
		print "Status 1: MAC ",bt[i]," wurde gefunden. Taster freigegeben (LED=blau)"
        	UpdateStatus()
	else:
          if ARG_DISPLAY == 1:
		print "Status: 0 (MAC ",bt[i]," wurde nicht gefunden (LED=rot)"
          doublecheck = 1
	
    time.sleep(varWaitTime)

except KeyboardInterrupt:
  destroy()


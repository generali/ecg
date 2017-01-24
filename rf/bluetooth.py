#!/usr/bin/env python

import bluetooth
import time
import sys

bt = ['CC:20:E8:64:0A:7F', '34:4D:AA:AD:7F:C0']


ARG_DISPLAY=0
for arg in sys.argv:
        if arg == "-display":
                ARG_DISPLAY=1


if ARG_DISPLAY == 1:
	print "DEMO: Bluetooth Tag"
	print ""
	print "Ausgabe:"


def Print(x):
        if x == 0:
		if ARG_DISPLAY == 1:
	                print '    ***********************'
       		        print '    *   Tuer geoeffnet!   *'
       	       	 	print '    ***********************'
try:
  while True:
    for i in range (len(bt)):
      Led(0)
      doublecheck = 0
      while doublecheck < 1:
        result = bluetooth.lookup_name(bt[i], timeout=3)
        if (result != None):
          # bluetooth device in range
          if ARG_DISPLAY == 1:
		print "Status 1: MAC ",bt[i]," wurde gefunden. Taster freigegeben (LED=blau)"
        else:
          if ARG_DISPLAY == 1:
		print "Status: 0 (MAC ",bt[i]," wurde nicht gefunden (LED=rot)"
          doublecheck = 1
except KeyboardInterrupt:
  destroy()


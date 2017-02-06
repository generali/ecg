#!/usr/bin/env python

import RPi.GPIO as GPIO
import bluetooth
import time
import sys

BtnPin = 18
Rpin   = 11
Gpin   = 13
Bpin   = 15

bt = ['CC:20:E8:64:0A:7F', '34:4D:AA:AD:7F:C0']


ARG_DISPLAY=0
for arg in sys.argv:
        if arg == "-display":
                ARG_DISPLAY=1


if ARG_DISPLAY == 1:
	print "DEMO: Bluetooth & Button press"
	print ""
	print "GPIO 17 (Pin 11)  -> LED R"
	print "GPIO 27 (Pin 13)  -> LED G"
	print "GPIO 22 (Pin 15)  -> LED B"
	print "GRND    (Pin 6 )  -> LED -"
	print ""
	print "GRND     (Pin 14) -> Button -"
	print "GPIO 3.3V(Pin 17) -> Button 5V"
	print "GPIO 24  (Pin 18) -> Button S"
	print ""
	print "Ausgabe:"


def setup():
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        GPIO.setup(Rpin, GPIO.OUT)     # Set Red Led Pin mode to output
        GPIO.setup(Gpin, GPIO.OUT)     # Set Green Led Pin mode to output
        GPIO.setup(Bpin, GPIO.OUT)     # Set Green Led Pin mode to output
        GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
#        GPIO.add_event_detect(BtnPin, GPIO.BOTH, callback=detect, bouncetime=200)

def Led(status):
        if status == 0:
                GPIO.output(Rpin, 1)
                GPIO.output(Gpin, 0)
                GPIO.output(Bpin, 0)
        if status == 1:
                GPIO.output(Rpin, 0)
                GPIO.output(Gpin, 0)
                GPIO.output(Bpin, 1)
        if status == 2:
                GPIO.output(Rpin, 0)
                GPIO.output(Gpin, 1)
                GPIO.output(Bpin, 0)

def Print(x):
        if x == 0:
		if ARG_DISPLAY == 1:
	                print '    ***********************'
       		        print '    *   Tuer geoeffnet!   *'
       	       	 	print '    ***********************'

#def detect(chn):
#        Led(GPIO.input(BtnPin))
#        Print(GPIO.input(BtnPin))

def destroy():
        GPIO.output(Gpin, GPIO.HIGH)       # Green led off
        GPIO.output(Rpin, GPIO.HIGH)       # Red led off
        GPIO.cleanup()                     # Release resource

#if __name__ == '__main__':     # Program start from here
#        setup()
#        try:
#                loop()
#        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
#                destroy()

setup()
try:
  while True:
    for i in range (len(bt)):
      Led(0)
      doublecheck = 0
      while doublecheck < 1:
        result = bluetooth.lookup_name(bt[i], timeout=3)
        if (result != None):
          Led(1)
          if ARG_DISPLAY == 1:
		print "Status 1: MAC ",bt[i]," wurde gefunden. Taster freigegeben (LED=blau)"
          if not (GPIO.input (BtnPin)):
            Led(2)
            if ARG_DISPLAY == 1:
		print "Status 2: MAC wurde gefunden & Taster wurde betaetigt (LED=gruen)"
            time.sleep (2)
        else:
          if ARG_DISPLAY == 1:
		print "Status: 0 (MAC ",bt[i]," wurde nicht gefunden (LED=rot)"
          doublecheck = 1
except KeyboardInterrupt:
  destroy()


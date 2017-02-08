#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time


PIR_PIN = 24

# ###########################################


GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

def MOTION(PIR_PIN):
               print "Motion Detected!"

print "PIR Module Test (CTRL+C to exit)"
time.sleep(2)
print "Ready"

try:
               GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=MOTION)
               while 1:
                              time.sleep(100)
except KeyboardInterrupt:
               print "Quit"
               GPIO.cleanup()

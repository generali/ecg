#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_ask import Ask, statement, convert_errors
import RPi.GPIO as GPIO
import logging

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.intent('GPIOControlIntent', mapping={'status': 'status', 'pin': 'pin'})

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

def gpio_control(status, pin):

    try:
	print "Trying to set PIN=%s" % pin
        pinNum = int(pin)
    except Exception as e:
        return statement('Pin number not valid.')

    GPIO.setup(pinNum, GPIO.OUT)

    if status in ['on', 'high']:    GPIO.output(pinNum, GPIO.HIGH)
    if status in ['off', 'low']:    GPIO.output(pinNum, GPIO.LOW)

    return statement('Turning pin {} {}'.format(pin, status))


if __name__ == '__main__':
	url = read_secret("json_push","url","/home/pi/ecg/")
	
	port = 5000 #the custom port you want
	app.run(host='0.0.0.0', port=port)

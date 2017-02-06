#!/usr/bin/python

import sqlite3
import ssl
import json
import requests
import urllib2

conn = sqlite3.connect('sensor_data.db')


ESC_LEVEL = 1
DB_FILE="sensor_data.db"
DB_SQL= " SELECT * FROM escalation_handling WHERE level = %s" % (ESC_LEVEL)

IFTTT_URL=""

# ----------------------------------------------------------------

conn = sqlite3.connect(DB_FILE)

def send_ifttt(parameter):
	print "ifttt (%s)" % (parameter)
	try:
		context = ssl._create_unverified_context()
		data = {
			'value1': parameter
		}
		req = urllib2.Request(IFTTT_URL)
		req.add_header('Content-Type', 'application/json')
		response = urllib2.urlopen(req, json.dumps(data), context=context)
	except:
		print "ERROR request"
		pass



def send_email():
	print "email"

def send_http():
	print "http"

def send_gpio():
	print "gpio"

def check_type(argument):
	switcher = {
		"ifttt": "send_ifttt",
		"email": "send_email",
		"http": "send_http",
		"gpio": "send_gpio",
	}
	return switcher.get(argument, "nothing")

cursor = conn.execute(DB_SQL)
for row in cursor:
	ESC_TYPE = row[1]
	ESC_ACTION = row[2]
	ESC_PARAMETER = row[3]

#	print "ACTION=%s" % (ESC_ACTION)

	method=check_type(ESC_TYPE) + "()"
	eval(method)

#print "Operation done successfully";
conn.close()


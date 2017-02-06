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

# ----------------------------------------------------------------

conn = sqlite3.connect(DB_FILE)

def read_secret(secret_name, mysecret, secret_path="./", secret_suffix=".secret"):
	secret_file="%s%s%s" % (secret_path, secret_name, secret_suffix)
	print "secret file: %s" % (secret_file)
	try:
    		config = {}
    		execfile(secret_file, config)
	except:
		print "Error import secret file..."
		pass
	return config[mysecret]

def send_ifttt(type, action, parameter):
	#print "ifttt (%s)" % (parameter)
	#print "ifttt url: %s" % (IFTTT_URL)
	try:
		context = ssl._create_unverified_context()
		data = {
			'value1': parameter
		}
		req = urllib2.Request(IFTTT_URL)
		req.add_header('Content-Type', 'application/json')
		response = urllib2.urlopen(req, json.dumps(data), context=context)
	except:
		print "ERROR in IFTTT request"
		pass



def send_email(type, action, parameter):
	print "email"

	import smtplib
	import string

	USER    = read_secret("email","user")
	PASS    = read_secret("email","password")
	HOST    = read_secret("email","server")
	SUBJECT = "Eskalation ElderyCare/Guard"
	TO      = action
	FROM    = "rpicontest@gmail.com"
	TEXT    = parameter
	PORT	= read_secret("email","port")

	print "user: %s" % (USER)
	print "password: %s" % (PASS)
	print "server: %s" % (HOST)
	print "port: %s" % (PORT)
	BODY = string.join((
	        "From: {0}".format(FROM),
	        "To: {0}".format(TO),
	        "Subject: {0}".format(SUBJECT),
	        "",
	        TEXT.encode('utf-8'),
	        ), "\r\n")

	server = smtplib.SMTP(HOST, PORT)
	server.set_debuglevel(1)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(USER, PASS)
	server.sendmail(FROM, TO, BODY)
	server.quit()

def send_http(type, action, parameter):
	print "http"

def send_gpio(type, action, paramneter):
	print "gpio"

def check_type(argument):
	switcher = {
		"ifttt": "send_ifttt",
		"email": "send_email",
		"http": "send_http",
		"gpio": "send_gpio",
	}
	return switcher.get(argument, "nothing")


IFTTT_URL = read_secret("ifttt_url", "url")

cursor = conn.execute(DB_SQL)
for row in cursor:
	ESC_TYPE = row[1]
	ESC_ACTION = row[2]
	ESC_PARAMETER = row[3]

#	print "ACTION=%s" % (ESC_ACTION)

	method=check_type(ESC_TYPE) + "(ESC_TYPE, ESC_ACTION, ESC_PARAMETER)"
	eval(method)

#print "Operation done successfully";
conn.close()


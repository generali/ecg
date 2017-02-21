#!/usr/bin/python
# -*- coding: utf-8 -*-

# #################################################################################################################
#
#	+++++ WORK IN PROGRESS +++++
#
#	Skript beinhaltet noch hart codierte Parameter; Datei dient dem Test der Eskalation, Änderungen bitte
#	nur nach Abspreche mit RF. Danke.
#
#################################################################################################################

import sqlite3
import ssl
import json
import requests
import urllib2
import time
import os.path
import RPi.GPIO as GPIO
from blessings import Terminal

ESC_LEVEL = 1
DB_FILE="sensor_data.db"
DB_SQL= " SELECT * FROM escalation_handling WHERE level = %s" % (ESC_LEVEL)

BuzzerPin = 11    # pin11
BuzzerSpeed = 1
# List of tone-names with frequency
BuzzerTones = {"c6":1047,
    "b5":988,
    "a5":880,
    "g5":784,
    "f5":698,
    "e5":659,
    "eb5":622,
    "d5":587,
    "c5":523,
    "b4":494,
    "a4":440,
    "ab4":415,
    "g4":392,
    "f4":349,
    "e4":330,
    "d4":294,
    "c4":262}
# Song is a list of tones with name and 1/duration. 16 means 1/16
BuzzerSong =    [
    ["e5",16],["eb5",16],
    ["e5",16],["eb5",16],["e5",16],["b4",16],["d5",16],["c5",16],
    ["a4",8],["p",16],["c4",16],["e4",16],["a4",16],
    ["b4",8],["p",16],["e4",16],["ab4",16],["b4",16],
    ["c5",8],["p",16],["e4",16],["e5",16],["eb5",16],
    ["e5",16],["eb5",16],["e5",16],["b4",16],["d5",16],["c5",16],
    ["a4",8],["p",16],["c4",16],["e4",16],["a4",16],
    ["b4",8],["p",16],["e4",16],["c5",16],["b4",16],["a4",4]
    ]

# ----------------------------------------------------------------


def read_secret(secret_name, mysecret, secret_path="./", secret_suffix=".secret"):
    # #######################################################
    # Liest Parameter aus der angegebenen Datei (.secret). Ermittelt
    # die Variable, die ebenfalls angegebenist und liefert deren Wert
    # zurück
    # #######################################################
    secret_file="%s%s%s" % (secret_path, secret_name, secret_suffix)
    # default value
    #config[mysecret]="ERROR"
    print "INFO: secret file: %s" % (secret_file)
    print "INFO: secret=%s" % (mysecret)
#    if os.path.isfile(secret_file):

    try:
        config = {}
        execfile(secret_file, config)
        print "INFO: %s=%s" % (mysecret,config[mysecret])
    except:
        print "ERROR: Error import secret file... (missing secret file?)"
        pass
    return config[mysecret]

# ###########################################################################
# ###########################################################################
# ###########################################################################
def send_ifttt(type, action, parameter):
	# #######################################################
	# Sendet eine Nachricht über IFTTT. URL für den Versand ist
	# in der Datei ifttt.secret mit der Variablen "url" gespeichert
	# #######################################################
	#print "ifttt (%s)" % (parameter)
	#print "ifttt url: %s" % (IFTTT_URL)
#    if read_secret("escalation","enable_ifttt") != 1:
#        return
    IFTTT_URL = read_secret("ifttt", "url")

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

# ###########################################################################
# ###########################################################################
# ###########################################################################
def send_email(type, action, parameter):
	# #######################################################
	# Sendet eine Nachricht per eMail. Die erforderlichen Parameter
	# für die Nutzung eines (erforderlichen) SMTP-Servers sind in
	# der Datei "email.secret" anzugeben (user, password, server, port)
	# #######################################################
#    if read_secret("escalation","enable_email") != 1:
#        return
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

#	print "user: %s" % (USER)
#	print "password: %s" % (PASS)
#	print "server: %s" % (HOST)
#	print "port: %s" % (PORT)
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

# ###########################################################################
# ###########################################################################
# ###########################################################################
def send_http(type, action, parameter):
	# #######################################################
	# Führt einen HTTP-Request aus
	# #######################################################
#    if read_secret("escalation","enable_http") != 1:
#        return
    print "http"

# ###########################################################################
# ###########################################################################
# ###########################################################################
def send_gpio(type, action, parameter):
	# #######################################################
	# Führt eine Änderung des Signals an dem angegebenen Port
	# des GPIO (BCM) aus.
	# #######################################################
#    if read_secret("escalation","enable_gpio") != 1:
#        return
    print "gpio"

# ###########################################################################
# ###########################################################################
# ###########################################################################
def buzzer_setup():
    GPIO.setmode(GPIO.BOARD) # Numbers GPIOs by physical location
    GPIO.setup(BuzzerPin, GPIO.OUT)

def buzzer_playTone(p,tone):
        # calculate duration based on speed and tone-length
    duration = (1./(tone[1]*0.25*BuzzerSpeed))

    if tone[0] == "p": # p => pause
        time.sleep(duration)
    else: # let's rock
        frequency = BuzzerTones[tone[0]]
        p.ChangeFrequency(frequency)
        p.start(0.5)
        time.sleep(duration)
        p.stop()

def buzzer_run():
    p = GPIO.PWM(BuzzerPin, 440)
    p.start(0.5)
    for t in BuzzerSong:
        buzzer_playTone(p,t)

def buzzer_destroy():
    GPIO.output(BuzzerPin, GPIO.HIGH)
    GPIO.cleanup()

def send_buzzer(type, action, parameter):
#    if read_secret("escalation","enable_buzzer") != 1:
#        return

	buzzer_setup()
	try:
		buzzer_run()
		GPIO.cleanup()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		buzzer_destroy()
		pass

# ###########################################################################
# ###########################################################################
# ###########################################################################
term = Terminal()

def term_init():
	print term.enter_fullscreen()
	print term.clear()

def term_exit():
	print term.exit_fullscreen()
	print term.move(0,term.height-1)

def term_escalation(fcode=7, bcode=0, title="", message="", delimiter="*"):
	term.clear()

	# background
	for x in xrange(20):
		with term.location(0,x):
			print term.on_color(bcode) + ' ' * int(term.width)

	# title
	title_pos=term.width/2-len(title)/2
	with term.location(title_pos,7):
		print term.on_color(bcode) + term.color(fcode) + term.bold + (delimiter * len(title))
	with term.location(title_pos,8):
		print term.on_color(bcode) + term.color(fcode) + term.bold + title
	with term.location(title_pos,9):
		print term.on_color(bcode) + term.color(fcode) + term.bold + (delimiter * len(title))
	# message
	with term.location(term.width/2-len(message)/2,12):
		print term.on_color(bcode) + term.color(fcode) + term.bold + message

def send_terminal(type, action, parameter):
#    if read_secret("escalation","enable_terminal") != 1:
#        return

    term_init()
    esc_fcolor, esc_bcolor, esc_title, esc_message = parameter.split('|')
#    term_escalation(read_secret("escalation","terminal_lvl"+ESC_LEVEL+"_fcolor"), read_secret("escalation","terminal_lvl"+ESC_LEVEL+"_bcolor"), read_secret("escalation","terminal_lvl"+ESC_LEVEL+"_title"), read_secret("escalation","terminal_lvl"+ESC_LEVEL+"_message"))
    term_escalation(esc_fcolor, esc_bcolor, esc_title, esc_message)
    term_exit()

# ###########################################################################
# ###########################################################################
# ###########################################################################
def check_type(argument):
	# #######################################################
	# Abfrage, welcher Typ von Schnittstelle genutzt werden soll
	# #######################################################
	switcher = {
		"ifttt": "send_ifttt",
		"email": "send_email",
		"http": "send_http",
		"gpio": "send_gpio",
		"buzzer": "send_buzzer",
        "terminal": "send_terminal",
	}
	return switcher.get(argument, "nothing")

conn = sqlite3.connect(DB_FILE)
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

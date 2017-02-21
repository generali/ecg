#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ASCII art: http://patorjk.com/software/taag/#p=display&f=Banner
# ############################################################################################
# ############################################################################################
# ##########
# ########## #     #    #    ######  ###    #    ######  #       #######  #####
# ########## #     #   # #   #     #  #    # #   #     # #       #       #     #
# ########## #     #  #   #  #     #  #   #   #  #     # #       #       #
# ########## #     # #     # ######   #  #     # ######  #       #####    #####
# ##########  #   #  ####### #   #    #  ####### #     # #       #             #
# ##########   # #   #     # #    #   #  #     # #     # #       #       #     #
# ##########    #    #     # #     # ### #     # ######  ####### #######  #####
# ##########
# ############################################################################################
# ############################################################################################


# ############################################################################################
# ############################################################################################
# ##########
# ##########  #####  #       ####### ######     #    #
# ########## #     # #       #     # #     #   # #   #
# ########## #       #       #     # #     #  #   #  #
# ########## #  #### #       #     # ######  #     # #
# ########## #     # #       #     # #     # ####### #
# ########## #     # #       #     # #     # #     # #
# ##########  #####  ####### ####### ######  #     # #######
# ##########
# ############################################################################################
# ############################################################################################

# ############################################################################################
# IMPORT LIBRARIES
# --- GENERIC ---
import argparse
import time
import math
import ssl
import time
import sys
from datetime import datetime
import socket
import threading
import ConfigParser
import logging
import sqlite3


# --- SENSOR SPECIFIC ---
import RPi.GPIO as GPIO
import bluetooth

# ############################################################################################
# PRE-DEFINITIOn OF VARIABLES
ARG_DISPLAY=0
SELECTED_SENSOR=""
SENSOR_QUALIFIER=""
SENSOR_FQN=""

# ############################################################################################
# GLOBAL PROCEDCURES
def show_banner():
    logger.info("#" * 80)
    logger.info("#####")
    logger.info("##### %s %s" % (APP_NAME, APP_VERSION))
    logger.info("#####")
    logger.info("#" * 80)
    logger.info("Hostname: %s" % (read_config("GLOBAL","hostname")))

def get_hostname():
    global ARG_DISPLAY

    #print "Checking hostname..."
    if socket.gethostname().find('.')>=0:
        name=socket.gethostname()
    else:
        name=socket.gethostbyaddr(socket.gethostname())[0]

    if name == "":
        #name=get_secret("hostname","hostname","/home/pi/ecg/")
        name=read_config("GLOBAL","hostname")

#    if ARG_DISPLAY == 1:
#        print "Hostname identified: %s" % (name)
    return name

def read_config(SECTION, KEY):
    config = ConfigParser.RawConfigParser()
    config.read('ecg.secret')

    # raw mode
    return config.get(SECTION, KEY)

def read_secret(secret_name, mysecret, secret_path="./", secret_suffix=".secret"):
    global ARG_DISPLAY

    # #######################################################
    # Liest Parameter aus der angegebenen Datei (.secret). Ermittelt
    # die Variable, die ebenfalls angegebenist und liefert deren Wert
    # zurück
    # #######################################################
    secret_file="%s%s%s" % (secret_path, secret_name, secret_suffix)
    # default value
    #config[mysecret]="ERROR"
    #print "INFO: secret file: %s" % (secret_file)
    if secret_file.is_file():
        try:
            config = {}
            execfile(secret_file, config)
#           print "INFO: %s=%s" % (mysecret,config[mysecret])
        except:
#           print "ERROR: Error import secret file... (missing secret file?)"
            pass
    else:
#       print "secret file missing"
        pass
    return config[mysecret]

def update_database(SENSOR_FQN, SENSOR_VALUE):
    global ARG_DISPLAY

    import json
    import urllib2

    try:
        context = ssl._create_unverified_context()

        url = read_secret("json_push","url","/home/pi/ecg/")
#       print 'URL=%s' % url

        data = {
            SENSOR_FQN: SENSOR_VALUE
        }

        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(data), context=context)
        # sleep to prevent massive database updates
    except:
        pass

# ############################################################################################
# ############################################################################################
# ##########
# ########## #######  #####   #####     #    #          #    ####### ### ####### #     #
# ########## #       #     # #     #   # #   #         # #      #     #  #     # ##    #
# ########## #       #       #        #   #  #        #   #     #     #  #     # # #   #
# ########## #####    #####  #       #     # #       #     #    #     #  #     # #  #  #
# ########## #             # #       ####### #       #######    #     #  #     # #   # #
# ########## #       #     # #     # #     # #       #     #    #     #  #     # #    ##
# ########## #######  #####   #####  #     # ####### #     #    #    ### ####### #     #
# ##########
# ############################################################################################
# ############################################################################################

def ESCALATION_SEND_ifttt(type, action, parameter):
	#print "ifttt (%s)" % (parameter)
	#print "ifttt url: %s" % (IFTTT_URL)
#    if read_secret("escalation","enable_ifttt") != 1:
#        return
    IFTTT_URL = read_config("IFTTT", "url")

    try:
        context = ssl._create_unverified_context()
        data = {
            'value1': parameter
        }
        req = urllib2.Request(IFTTT_URL)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(data), context=context)
    except:
        logger.error("ERROR in IFTTT request")
        pass

def ESCALATION_SEND_email(type, action, parameter):
	# #######################################################
	# Sendet eine Nachricht per eMail. Die erforderlichen Parameter
	# für die Nutzung eines (erforderlichen) SMTP-Servers sind in
	# der Datei "email.secret" anzugeben (user, password, server, port)
	# #######################################################
#    if read_secret("escalation","enable_email") != 1:
#        return
    import smtplib
    import string

    USER    = read_config("EMAIL","user")
    PASS    = read_config("EMAIL","password")
    HOST    = read_config("EMAIL","server")
    SUBJECT = read_config("EMAIL","subject")
    TO      = action
    FROM    = read_config("EMAIL","from")
    TEXT    = parameter
    PORT	= read_config("EMAIL","port")

    logger.debug("user: %s" % (USER))
    logger.debug("password: %s" % (PASS))
    logger.debug("server: %s" % (HOST))
    logger.debug("port: %s" % (PORT))
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

def ESCALATION_SEND_http(type, action, parameter):
    logger.debug("HTTP request")

# ###########################################################################
# ###########################################################################
# ###########################################################################
def ESCALATION_SEND_gpio(type, action, parameter):
    logger.debug("GPIO request")

def ESCALATION_checktype(argument):
	# #######################################################
	# Abfrage, welcher Typ von Schnittstelle genutzt werden soll
	# #######################################################
	switcher = {
		"ifttt": "ESCALATION_SEND_ifttt",
		"email": "ESCALATION_SEND_email",
		"http": "ESCALATION_SEND_http",
		"gpio": "ESCALATION_SEND_gpio",
#		"buzzer": "ESCALATION_SEND_buzzer",
#        "terminal": "ESCALATION_SEND_terminal",
	}
	return switcher.get(argument, "nothing")

def ESCALATION_init():
    conn = sqlite3.connect(read_config("DATABASE","file"))
    DB_SQL= " SELECT * FROM escalation_handling WHERE level = %s" % (read_config("ESCALATION","level"))
    cursor = conn.execute(DB_SQL)
    for row in cursor:
    	ESC_TYPE = row[1]
    	ESC_ACTION = row[2]
    	ESC_PARAMETER = row[3]

    	logger.debug("ACTION=%s" % (ESC_ACTION))

    	method=ESCALATION_checktype(ESC_TYPE) + "(ESC_TYPE, ESC_ACTION, ESC_PARAMETER)"
    	eval(method)

    logger.debug("Operation done successfully")
    conn.close()



# ############################################################################################
# ############################################################################################
# ##########
# ##########  #####  ####### #     #  #####  ####### ######   #####
# ########## #     # #       ##    # #     # #     # #     # #     #
# ########## #       #       # #   # #       #     # #     # #
# ##########  #####  #####   #  #  #  #####  #     # ######   #####
# ##########       # #       #   # #       # #     # #   #         #
# ########## #     # #       #    ## #     # #     # #    #  #     #
# ##########  #####  ####### #     #  #####  ####### #     #  #####
# ##########
# ############################################################################################
# ############################################################################################

# ############################################################################################
# MOTION
def SENSOR_MOTION_action(PIR_PIN):
    global ARG_DISPLAY

    logger.info(time.strftime("%b %d %Y %H:%M:%S", time.gmtime())+ " - Motion Detected!")

    SENSOR_FQN = get_hostname() + "." + SENSOR_MOTION_NAME
    update_database(SENSOR_FQN, 1)
    time.sleep(1)

def SENSOR_MOTION_init(arg):
    global ARG_DISPLAY

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR_MOTION_BCM_PIN1, GPIO.IN)
    logger.info("PIR Module Test (CTRL+C to exit)")
    logger.info("")
    logger.info("GPIO 27 (Pin 13) -> Signal Motion")
    logger.info("VCC     (Pin 4) -> Motion Sensor VCC")
    logger.info("GRND    (Pin 6) -> Motion Sensor GRND")

    GPIO.add_event_detect(SENSOR_MOTION_BCM_PIN1, GPIO.RISING, callback=SENSOR_MOTION_action)
    this_thread = threading.currentThread()
    while getattr(this_thread, "do_run", True):
        time.sleep(1)

#    try:
#        GPIO.add_event_detect(SENSOR_MOTION_BCM_PIN1, GPIO.RISING, callback=SENSOR_MOTION_action)
#        while 1:
#            time.sleep(1)
#    except KeyboardInterrupt:
#        GPIO.cleanup()

# ############################################################################################
# BLUETOOTH
def SENSOR_BLUETOOTH_init(arg):
    global ARG_DISPLAY

    this_thread = threading.currentThread()
    while getattr(this_thread, "do_run", True):
        # Try to gather information from the desired device.
        # We're using two different metrics (readable name and data services)
        # to reduce false negatives.
        state = bluetooth.lookup_name(SENSOR_BLUETOOTH_CHECK, timeout=20)
        services = bluetooth.find_service(address=SENSOR_BLUETOOTH_CHECK)
        # Flip the LED pin on or off depending on whether the device is nearby
        if state == None and services == []:
            logger.info(time.strftime("%b %d %Y %H:%M:%S", time.gmtime())+ " - No device in range!")
        else:
            logger.info(time.strftime("%b %d %Y %H:%M:%S", time.gmtime())+ " - Device detected!")
            SENSOR_FQN = get_hostname() + "." + SENSOR_BLUETOOTH_NAME
            update_database(SENSOR_FQN, 1)
        # Arbitrary wait time
        time.sleep(5)

# ############################################################################################
# Dashbutton
def SENSOR_DASHBUTTON_init():
    global ARG_DISPLAY
    print(sniff(iface=SENSOR_DESHBUTTON_INTERFACE, prn=SENSOR_BLUETOOTH_action, filter="arp", store=0))

def SENSOR_DASHBUTTON_action(pkt):
    mac_actions = { SENSOR_DASHBUTTON_CHECK : SENSOR_BLUETOOTH_action2 }
    mac_list = list(mac_actions.keys())

    logger.info('method init...')
    logger.info('hw.src=' + pkt[ARP].hwsrc)
    logger.info('hw.psrc=' + pkt[ARP].psrc)
    if pkt[ARP].op == 1: #who-has (request)
        if pkt[ARP].hwsrc in mac_list : # this is the first button MAC address
            mac_actions[pkt[ARP].hwsrc](pkt[ARP].hwsrc)
        else:
            logger.info("ARP Probe from unknown device: " + pkt[ARP].hwsrc)

def SENSOR_DASHBUTTON_action2(mac) :
    logger.info('#########################################################')
    logger.info('### Amazon Dash Button #1 pressed (' + mac + ') ###')
    logger.info('#########################################################')

    SENSOR_FQN = get_hostname() + "." + SENSOR_DASHBUTTON_NAME
    update_database(SENSOR_FQN, 1)

# ############################################################################################
# ...

# ############################################################################################
# ...
def SENSOR_MOTION_thread():
    try:
        thread_motion = threading.Thread(target=SENSOR_MOTION_init, args=("task",), kwargs={})
        thread_motion.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        thread_motion.do_run=False
        thread_motion.join()

def SENSOR_BLUETOOTH_thread():
    try:
        thread_bluetooth = threading.Thread(target=SENSOR_BLUETOOTH_init, args=("task",), kwargs={})
        thread_bluetooth.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        thread_bluetooth.do_run=False
        thread_bluetooth.join()



def nothing():
    logger.info("kein Sensor ausgewählt")

# ############################################################################################
# ############################################################################################
# ##########
# ########## ### #     # ### #######
# ##########  #  ##    #  #     #
# ##########  #  # #   #  #     #
# ##########  #  #  #  #  #     #
# ##########  #  #   # #  #     #
# ##########  #  #    ##  #     #
# ########## ### #     # ###    #
# ##########
# ############################################################################################
# ############################################################################################

SENSOR_MOTION_NAME = read_config("MOTION","name")
SENSOR_MOTION_BCM_PIN1=27
PIR_PIN_BCM = 27

SENSOR_BLUETOOTH_NAME = read_config("BLUETOOTH","name")
SENSOR_BLUETOOTH_CHECK = read_config("BLUETOOTH","mac")
SENSOR_BLUETOOTH_WAIT = 30

SENSOR_DASHBUTTON_NAME = read_config("DASHBUTTON","name")
SENSOR_DASHBUTTON_CHECK = read_config("DASHBUTTON","mac")
SENSOR_DESHBUTTON_INTERFACE = read_config("DASHBUTTON","interface")

ESCALATION_NAME = read_config("ESCALATION","name")



parser = argparse.ArgumentParser()
parser.add_argument('-s', "--sensor", action='store', dest='sensorname',
                    help='Angabe des zu verwendenden Sensors ([%s])' % (SENSOR_MOTION_NAME))
parser.add_argument('-v', "--verbose", action='store_true', default=False, dest="ARG_DISPLAY",
					help='Anzeige der Bildschirmausgabe aktivieren')
#parser.add_argument('-f', action='store_const', dest="varWaitTime",
#                    help='Beschleunigte Wartezeit zwischen den Messungen (5 Sekunden)')
parser.add_argument('--version', action='version', version='%(APP_NAME)s APP_VERSION')
results = parser.parse_args()

ARG_DISPLAY=results.ARG_DISPLAY
SELECTED_SENSOR=results.sensorname





if __name__ == '__main__':
    # ############################################################################################
    # GENERIC VARIABLES
    APP_NAME = read_config("GLOBAL","app_name")
    APP_VERSION = read_config("GLOBAL", "app_version")

    # ############################################################################################
    # LOGGING FACILITY
    logging.basicConfig()
    logger = logging.getLogger(APP_NAME)
    level = logging.getLevelName(read_config("LOG","level"))
    logger.setLevel(level)
    hdlr = logging.FileHandler(read_config("LOG", "logfile"))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    # ############################################################################################
    # INTRO
    show_banner()

    logger.info("NAME= %s" % (SENSOR_MOTION_NAME))
    logger.info("SENSOR: %s" % (SELECTED_SENSOR))
    SENSOR_QUALIFIER = get_hostname()

    switcher = {
        SENSOR_MOTION_NAME: SENSOR_MOTION_init,
        SENSOR_BLUETOOTH_NAME: SENSOR_BLUETOOTH_init,
        ESCALATION_NAME: ESCALATION_init,
    }
    # Get the function from switcher dictionary
    func = switcher.get(SELECTED_SENSOR, "nothing")

    if SELECTED_SENSOR == "motion":
        SENSOR_MOTION_thread()

    if SELECTED_SENSOR == "bluetooth":
        SENSOR_BLUETOOTH_thread()

    if SELECTED_SENSOR == "escalation":
	ESCALATION_init()

#ESCALATION_init()
#    try:
#        if func != "nothing":
#            # einzelnen Sensor starten
##            func("")
#            thr1 = threading.Thread(target=func, args=("task",), kwargs={})
#            while 1:
#                time.sleep(1)
#        else:
#            # alle Sensoren starten
#            thr1 = threading.Thread(target=SENSOR_MOTION_init, args=("task",), kwargs={})
#            thr2 = threading.Thread(target=SENSOR_BLUETOOTH_init, args=("task",), kwargs={})
#            while 1:
#                time.sleep(1)
#
#    except KeyboardInterrupt:
#        print "EXIT"
#        thr1.do_run=False
#        thr2.do_run=False

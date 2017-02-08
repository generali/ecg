#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tip: https://bob.igo.name/wp-content/uploads/2015/10/AmazonDash.pdf
# Tip: http://hypfer.de/blog/2016/09/02/amazon-dash-button-zweckentfremden-ohne-arp-1n/

SENSOR_TYPE = "dashbutton"

# ##############################################

import logging # for the following line
import os
import rrdtool
import time
import math
import ssl
import time
import sys
from datetime import datetime


ARG_DISPLAY=0
for arg in sys.argv:
        if arg == "-display":
                ARG_DISPLAY=1

logging.getLogger("scapy.runtime").setLevel(logging.ERROR) # suppress IPV6 warning on startup

from scapy.all import * # for sniffing for the ARP packets
import requests # for posting to the IFTTT Maker Channel

# it takes a minute for the scapy sniffing to initialize, so I print this to know when it's actually ready to go
if ARG_DISPLAY == 1:
	print('')
	print('####################################################################################################')
	print('### ACHTUNG: ipforwarding MUSS deaktiviert sein, da sonst Bestellungen ausgeloest werden koennen!!!')
	print('### (oder ggf. Zugriff der MAC auf Internet per iptables sperren)')
    print('####################################################################################################')
    print('Init Amazon Dash Button sniffer... done.')

def get_hostname():
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

def button1_pressed(mac) :
    if ARG_DISPLAY == 1:
        print('')
        print('#########################################################')
        print('### Amazon Dash Button #1 pressed (' + mac + ') ###')
        print('#########################################################')

    try:
        context = ssl._create_unverified_context()

        url = read_secret("json_push","url","/home/pi/ecg/")
#       print 'URL=%s' % url

        import json
        import urllib2

        SENSOR_FQN = SENSOR_QUALIFIER + "." + SENSOR_TYPE
        data =
            'SENSOR_FQN': 1
        }

        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, json.dumps(data), context=context)
    except:
        pass

def arp_display(pkt):
    mac_actions = { 'ac:63:be:c6:28:af' : button1_pressed }
    mac_list = list(mac_actions.keys())

    if ARG_DISPLAY == 1:
        print('------------------')
        print('method init...')
        print('hw.src=' + pkt[ARP].hwsrc)
        print('hw.psrc=' + pkt[ARP].psrc)
    if pkt[ARP].op == 1: #who-has (request)
        if pkt[ARP].hwsrc in mac_list : # this is the first button MAC address
            mac_actions[pkt[ARP].hwsrc](pkt[ARP].hwsrc)
        else:
            if ARG_DISPLAY == 1:
                print("ARP Probe from unknown device: " + pkt[ARP].hwsrc)

SENSOR_QUALIFIER = get_hostname()
if ARG_DISPLAY == 1:
    print "DEMO: " + SENSOR_TYPE
    print ("#" * 40)
    print "Hostname: " + SENSOR_QUALIFIER
    print "Ausgabe:"

print(sniff(iface="wlan1", prn=arp_display, filter="arp", store=0))

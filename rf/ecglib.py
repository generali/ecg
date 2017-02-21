#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bluetooth
import time
import sys
import requests
import ssl
import socket
import os.path

def get_hostname():
    #print "Checking hostname..."
    if socket.gethostname().find('.')>=0:
        name=socket.gethostname()
    else:
        name=socket.gethostbyaddr(socket.gethostname())[0]
    print "Hostname identified: %s" % (name)
    return name

def read_secret(secret_name, mysecret, secret_path="./", secret_suffix=".secret"):
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
#                   		print "INFO: %s=%s" % (mysecret,config[mysecret])
        except:
#	         	print "ERROR: Error import secret file... (missing secret file?)"
            pass
    else:
#        print "secret file missing"
        pass
    return config[mysecret]

hostname = get_hostname()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse, json
import sqlite3
import re
import cgi
import logging
import sys
import time
import datetime

# ######################################################

# IP-Adresse, auf der der Webservice horcht (z.B. localhost, 127.0.0.1, 10.0.0.54, my_raspberry.no-ip.com, ...)
# ACHTUNG: Zugriff von andere IPs als der angegebenen werden aktuell nicht unterstuetzt
SERVER_IP ="0.0.0.0"
# Port, auf dem der Webservice horcht
SERVER_PORT = 8080

# part of URL to save sensor information. call e.g. http://ecg:8080/collector/
SERVER_PATH_WRITE='collector/'
#SERVER_PATH_READ='sensors/read/'

# Konfiguration der Datenbank
DATABASE_PATH = "/home/pi/ecg/sensor_data.db"
DB_TABLE_SENSOR_DATA = "sensor_data"

# sleep time between database operations
DATABASE_SLEEP=.5
# ######################################################

ARG_DISPLAY=0
ARG_LOGFILE=0
for arg in sys.argv:
    if arg == "-display":
        ARG_DISPLAY=1
    if arg == "-log":
        ARG_LOGFILE=1
    if arg == "-fast":
        varWaitTime=5


def  do_log(mtype, message):
    if ARG_DISPLAY == 0:
        if mtype == "WARNING":
            print mtype + ": " + message
        if mtype == "ERROR":
            print mtype + ": " + message
        if mtype == "CRITICAL":
            print mtype + ": " + message

    if ARG_DISPLAY == 1:
        print mtype + ": " + message


    if ARG_LOGFILE == 1:
        logger = logging.getLogger('ecg_webserver')
        hdlr = logging.FileHandler('/home/pi/ecg/webserver.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)

        logger.setLevel(logging.WARNING)

        if mtype == 'ERROR':
            logger.error(message)
        if mtype == "WARNING":
            logger.warning(message)
        if mtype == "INFO":
            logger.info(message)

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
#        if None != re.search('/' + SERVER_PATH_READ + '*', self.path):
#            parsed_path = urlparse.urlparse(self.path)
#            conn = sqlite3.connect(DATABASE_PATH)
#
#            cursor = conn.execute("SELECT exectime,sensor_key, sensor_value from %s" % (DB_TABLE_SENSOR_DATA))
#            cursor = conn.execute('SELECT exectime, sensor_value FROM %s WHERE sensor_key LIKE \"%temperature%\" AND (strftime(\'%s\',datetime(\'now\',\'localtime\'))-strftime(\'%s\',exectime)<600) ORDER BY exectime' % (DB_TABLE_SENSOR_DATA))
#
#            message = "<html><head><style>thead {color:grey;} table,th,td {border:1px solid black;}</style></head><body><table border=1><thead><tr><th>Zeit</th><th>Sensor</th><th>Wert</th></tr></thead>"
#            for row in cursor:
#                message+= "<tr><td>%s</td>" % (row[0])
#                message+= "<td>%s</td>" % (row[1])
#                message+= "<td>%s</td></tr>" % (row[2])
#            conn.close()
#            message+="</table></body></html>"
#
#            self.send_response(200)
#            self.end_headers()
#            self.wfile.write(message)
	pass
        return

    def do_POST(self):
        if None != re.search('/' + SERVER_PATH_WRITE + '*', self.path):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            do_log ("INFO","directory call fine")
            if ctype == 'application/json':
                do_log("INFO","everything fine")
                # do here some checks or executions if json specific
                pass

            content_len = int(self.headers.getheader('content-length'))
            post_body = self.rfile.read(content_len)
            self.send_response(200)
            self.end_headers()

            do_log("INFO","#############################################################")
            do_log("INFO","##### new request")
            do_log("INFO","#############################################################")
            do_log ("INFO", "request received")
            data = json.loads(post_body)
#            do_log ("INFO", "Establish database connection")
            conn_ins = sqlite3.connect(DATABASE_PATH)

            for key, value in data.items():
		LOGSTRING="Data submitted - Key={0}, value={0}".format(key, value)
                do_log("INFO", LOGSTRING)
                SENSOR_TABLE = "sensor_data"
                SENSOR_TABLE_TYPE = "sensor_type"
                SENSOR_VIEW = "v.sensor." + key

#                LOGSTRING="Sensor type table = {0}".format(SENSOR_TABLE_TYPE)
#                do_log("INFO", LOGSTRING)

                time.sleep(DATABASE_SLEEP)
                try:
#                    conn_ins = sqlite3.connect(DATABASE_PATH)
                    SQL_CMD="INSERT OR IGNORE INTO \"%s\" (SENSOR_KEY, SENSOR_ACTIVE) VALUES (\"%s\",0)" % (SENSOR_TABLE_TYPE, key)
                    do_log ("INFO", SQL_CMD)
                    conn_ins.execute(SQL_CMD)
                    conn_ins.commit()
                except:
                    do_log ("WARNING", "Error creating sensor type '{0}'".format(key))
                    pass


                do_log("INFO", "Sensor view={0}".format(SENSOR_VIEW))
                time.sleep(DATABASE_SLEEP)
                try:
#                    conn_ins = sqlite3.connect(DATABASE_PATH)
                    SQL_CMD="DROP VIEW IF EXISTS \"%s\"" % (SENSOR_VIEW)
                    do_log ("INFO", SQL_CMD)
                    conn_ins.execute(SQL_CMD)
                    conn_ins.commit()
                except:
                    do_log ("WARNING", "Error dropping sensor view '{0}'".format(SENSOR_VIEW))
                    pass
#
                time.sleep(DATABASE_SLEEP)
                try:
                    SQL_CMD="CREATE VIEW \"%s\" AS SELECT exectime, sensor_key, sensor_value FROM \"sensor_data\" WHERE sensor_key = \"%s\"" % (SENSOR_VIEW, key)
                    do_log ("INFO", SQL_CMD)
                    conn_ins.execute(SQL_CMD)
                    conn_ins.commit()
                    self.wfile.write(value)
                except:
                    LOGSTRING="Error creating sensor view \"{0}\". Already there?".format(SENSOR_VIEW)
		    do_log ("WARNING", LOGSTRING)
                    pass

                time.sleep(DATABASE_SLEEP)
                try:
#                    conn_ins = sqlite3.connect(DATABASE_PATH)
                    SQL_CMD="INSERT INTO '%s' (SENSOR_KEY,SENSOR_VALUE) VALUES ('%s', '%s');" % (SENSOR_TABLE, key, value)
                    do_log ("INFO", SQL_CMD)
                    conn_ins.execute(SQL_CMD)
                    conn_ins.commit()
                    self.wfile.write(value)
                except:
#               Error in SQL
		    LOGSTRING="Error inserting data in table '%s' with %s=%s" % (SENSOR_TABLE, key, value)
                    do_log ("ERROR", LOGSTRING)
                    pass

        conn_ins.close()
        return

if __name__ == '__main__':
    # ###########################################

    from BaseHTTPServer import HTTPServer
    server = HTTPServer((SERVER_IP, SERVER_PORT), GetHandler)
    do_log("INFO",'Python Simple Webserver')
    do_log("INFO",'===============================================================================')
#    do_log("INFO",'Starting server at http://{0}:{0}'.format(SERVER_IP,SERVER_PORT))
#    do_log("INFO",'')
#    do_log("INFO",'Publish data via JSON (e.g. curl via commandline):')
#    do_log("INFO",'=> curl -d \'{"RPI3.temperature":35.55}\' {0}:{0}/{0} -H "Content-Type: application/json"'.format(SERVER_IP,SERVER_PORT,SERVER_PATH_WRITE))
#    do_log("INFO",'     NAME OF SENSOR : RPI3.temperature')
#    do_log("INFO",'     VALUE OF SENSOR: 35.55 (as numeric)')
#    do_log("INFO",'     VALUE OF SENSOR: "35.55" (as string)')
#    do_log("INFO",'')
#    do_log("INFO",'===============================================================================')
    server.serve_forever()

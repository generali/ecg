#!/usr/bin/python


from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse, json
import sqlite3
import re
import cgi

# ######################################################

# IP-Adresse, auf der der Webservice horcht (z.B. localhost, 127.0.0.1, 10.0.0.54, my_raspberry.no-ip.com, ...)
# ACHTUNG: Zugriff von andere IPs als der angegebenen werden aktuell nicht unterstuetzt
SERVER_IP ="localhost"
# Port, auf dem der Webservice horcht
SERVER_PORT = 8080

SERVER_PATH_WRITE='sensors/write/'
SERVER_PATH_READ='sensors/read/'

# Konfiguration der Datenbank
DATABASE_PATH = "sensor_data.db"
DB_TABLE_SENSOR_DATA = "sensor_data"

# ######################################################

class GetHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if None != re.search('/' + SERVER_PATH_READ + '*', self.path):
            parsed_path = urlparse.urlparse(self.path)
            conn = sqlite3.connect(DATABASE_PATH)

            cursor = conn.execute("SELECT exectime,sensor_key, sensor_value from %s" % (DB_TABLE_SENSOR_DATA))
            message = "<html><head><style>thead {color:grey;} table,th,td {border:1px solid black;}</style></head><body><table border=1><thead><tr><th>Zeit</th><th>Sensor</th><th>Wert</th></tr></thead>"
            for row in cursor:
                message+= "<tr><td>%s</td>" % (row[0])
                message+= "<td>%s</td>" % (row[1])
                message+= "<td>%s</td></tr>" % (row[2])
            conn.close()
            message+="</table></body></html>"

            self.send_response(200)
            self.end_headers()
            self.wfile.write(message)

        return

    def do_POST(self):
        if None != re.search('/' + SERVER_PATH_WRITE + '*', self.path):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            print "INFO: directory call fine"
            if ctype == 'application/json':
                print "INFO: everything fine"		

            content_len = int(self.headers.getheader('content-length'))
            post_body = self.rfile.read(content_len)
            self.send_response(200)
            self.end_headers()

            data = json.loads(post_body)
            for key, value in data.items():
#                print "Key=%s, Value=%s" % (key, value)
                try:
                    conn_ins = sqlite3.connect(DATABASE_PATH)
                    SQL_CMD="INSERT INTO %s (SENSOR_KEY,SENSOR_VALUE) VALUES ('%s', '%s');" % (DB_TABLE_SENSOR_DATA, key, value)
#                    print SQL_CMD
                    conn_ins.execute(SQL_CMD)
                    conn_ins.commit()
                    conn_ins.close()
                    self.wfile.write(value)
                except:
#               Error in SQL
                    print "Error in JSON?"
                    pass
        return

if __name__ == '__main__':
    # ###########################################

    from BaseHTTPServer import HTTPServer
    server = HTTPServer((SERVER_IP, SERVER_PORT), GetHandler)
    print 'Python Simple Webserver'
    print '==============================================================================='
    print 'Starting server at http://%s:%s' % (SERVER_IP, SERVER_PORT)
    print ''
    print 'Publish data via JSON (e.g. curl via commandline):'
    print '=> curl -d \'{"RPI3.temperature":35.55}\' %s:%s/%s -H "Content-Type: application/json"' % (SERVER_IP, SERVER_PORT, SERVER_PATH_WRITE)
    print '     NAME OF SENSOR : RPI3.temperature'
    print '     VALUE OF SENSOR: 35.55 (as numeric)'
    print '     VALUE OF SENSOR: "35.55" (as string)'
    print ''
    print 'Display sensor data via webbrowser:'
    print '=> http://%s:%s/%s' % (SERVER_IP, SERVER_PORT, SERVER_PATH_READ)
    print ''
    print '==============================================================================='
    server.serve_forever()

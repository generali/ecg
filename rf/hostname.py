#!/usr/bin/env python

import socket

print "Checking hostname..."
if socket.gethostname().find('.')>=0:
    name=socket.gethostname()
else:
    name=socket.gethostbyaddr(socket.gethostname())[0]

print "python hostname={0}".format(name)

#! /usr/bin/env python
# encoding: windows-1250
#
# Res Andy 

import os, re, sys, time, socket
from settings import camaddr
from settings import camport

srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.connect((camaddr, camport))

srv.send(b'{"msg_id":257,"token":0}')

data = srv.recv(512)
if b"rval" in data:
	token = re.findall(b'"param": (.+) }',data)[0]	
else:
	data = srv.recv(512)
	if b"rval" in data:
		token = re.findall(b'"param": (.+) }',data)[0]	


tosend = b'{"msg_id":513,"token":%s}' %token
srv.send(tosend)
srv.recv(512)

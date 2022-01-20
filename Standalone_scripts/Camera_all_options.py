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



tosend = b'{"msg_id":3,"token":%s}' %token 
srv.send(tosend)

while 1:
	conf = srv.recv(4096)
	if b"param" in conf:
		break

conf = conf[37:]

myconf = conf.split(b",")

for mytag in myconf:
	if len(mytag) > 5:
		paramname = re.findall (b'{ "(.+)": "', mytag)[0]
		tosend = b'{"msg_id":3,"token":%s,"param":"%s"}' %(token, paramname) 
		srv.send(tosend)
		print(srv.recv(8192))


print("_____________________________________________")
print()
print("press CTRL+C to close")

while 1:
	time.sleep(1)

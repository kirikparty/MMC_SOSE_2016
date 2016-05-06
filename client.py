#!/usr/bin/python
import socket
import sys
import time
import datetime
import IN

timer = time.time() #if sys.platform == Win32 else time.time
from datetime import datetime
timer2=datetime.now().strftime("%H:%M:%S.%f")

def alert(msg):
	print "Unable to connect to server. Please check the below exception."
	print >>sys.stderr, msg
	sys.exit(1)

if len(sys.argv) == 3:
	hostname = sys.argv[1]
	port = int(sys.argv[2])
	print hostname, '\n',port
else:
	print 'Please only enter the hostname and port, nothing more! Usage: python script.py HOSTNAME PORT'
	sys.exit(1)
if hostname[0] == '1':
	print 'PLease enter the hostname in INET Address form and not in IP Address V4 form.'
	sys.exit(1)
buffer_type = input("Enter your choice, 1 for short packet payload and 2 for large packet payload: ")
if buffer_type == 1:
	buffer_size = 800
elif buffer_type == 2:
	buffer_size = 1500
else:
	print 'Please enter only 1 or 2!! Exiting program!'
	sys.exit(1)
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,buffer_size)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,buffer_size)

except socket.error:
	print 'Failed to create socket!'
	sys.exit(1)
try:
	host = socket.gethostbyname(hostname)
except socket.gaierror:
	print 'There was an error resolving the host. Please enter correct hostname as a string and port as a number, as provided by service.'
	sys.exit(1)

print 'The host', hostname, 'has been resolved as', host, ':', port
print 'Connecting to host now...'

#for i in range(0,200):
try:

	s.connect((host, port))
	timer_start = datetime.now()
	s.settimeout(20.0)

	print 'Connection started at', timer_start
	try:
		s.send('TEST')
	except Exception, e:
		print 'Cannot send test data. Please check connection.'
		alert(e)
	try:
		data0 = s.recv(buffer_size)
		print 'recieved', data0, ' Connection established. Sending packets now...'
	except socket.error:
		print 'Unable to establish connection. Please try again later. Exiting now.'
		sys.exit(1)
		
#for i in range (0,2):
	try:
		a = 'A'*(buffer_size-30)
		print len(a)
		s.send(a);
		timer_send1=datetime.now()
		b= 'B'*(buffer_size-30)
		print len(b)
		s.send(b)
		timer_send2=datetime.now()
		print '1st TEST SENT AT', timer_send1
		print '2nd TEST SENT AT', timer_send2
	except socket.error:
		print 'Cannot send data. Please check connection'
		sys.exit(1) 

	try:
		data1 = s.recv(buffer_size)
		timer_recv1= datetime.now()
		print 'reccieved', data1, 'at time', timer_recv1
		data2 = s.recv(buffer_size)	
		timer_recv2=datetime.now()
		print 'recieved', data2, 'at time', timer_recv2 
	except socket.error, socket.timeout:
		print 'Could not recieve from server! Please check if socket was correctly given.'
		sys.exit(1)
	print 'The packet dispersion is', timer_recv2-timer_recv1
except Exception, e:
	alert(e)

print 'Connection to', hostname, 'was succesful. Statistics to follow'
s.shutdown(socket.SHUT_RDWR)
s.close()

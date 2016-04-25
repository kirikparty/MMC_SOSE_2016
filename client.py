#!/usr/bin/python
import socket
import sys
import time

timer = time.time #if sys.platform == Win32 else time.time

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
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print 'Failed to create socket!'
	sys.exit(1)
#host = socket.gethostname()
#port = 12345
try:
	host = socket.gethostbyname(hostname)
except socket.gaierror:
	print 'There was an error resolving the host. Please enter correct hostname as a string and port as a number, as provided by service.'
	sys.exit(1)

print 'The host', hostname, 'has been resolved as', host, ':', port
print 'Connecting to host now...'

for i in range(0,200):
	try:
		try:
		#s.bind((host, port)) #Used here to see if we are actually connecting to the right port.
				     #Commenting the above line will result in connection to an unknown
				     #port getting accepted.
			s.connect((host, port))
		except socket.error, exc:
			print 'Connection to host failed! Please check if hostname and port number are correct.'
    			print "Caught exception socket.error : %s" %exc
			sys.exit(1)

		timer_start= timer()
		s.settimeout(5.0)

		print 'Connection started at', timer_start
		try:
			s.send('TEST')
			timer_send=timer()
			print 'TEST SENT AT', timer_send
		except socket.error:
			print 'Cannot send data. Please check connection'
			sys.exit(1) 

		try:
			data = s.recv(1024)	#how DO I TIME IT OUT HERE????
			timer_recv = timer()
		#	while data:
		#		data = s.recv(1024)
		except socket.error, socket.timeout:
			print 'Could not recieve from server! Please check if socket was correctly given.'
			sys.exit(1)
	
	
		print 'I have recieved', data, 'from the server, at time', timer_recv
		i=i+1

	except Exception, e:
		alert(e)

print 'Connection to', hostname, 'was succesful. Statistics to follow'
print 'Total round trip time is', timer_recv-timer_send
#print s.recv(1024)
s.close

#!/usr/bin/python
import socket
import sys
import time
import datetime

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
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,1024)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,1024)

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

#for i in range(0,200):
try:
	try:
	#s.bind((host, port)) #Used here to see if we are actually connecting to the right port.
			     #Commenting the above line will result in connection to an unknown
			     #port getting accepted.
		s.connect((host, port))
#		s.setsocketopt(SOL_SOCKET,SO_SNDBUF,8192)
#		s.setsocketopt(SOL_SOCKET, SO_RCVBUF, 8192)
	except socket.error, exc:
		print 'Connection to host failed! Please check if hostname and port number are correct.'
  		print "Caught exception socket.error : %s" %exc
		sys.exit(1)

	#timer_start= timer2
	timer_start = datetime.now()#.strftime("%H:%M:%S.%f")
	s.settimeout(20.0)

	print 'Connection started at', timer_start
#for i in range (0,2):
	try:
		s.send('TEST')	#How to send two packets back to back? Close socket and reopen socket
				#again? Gotta ask the tutor.
		timer_send1=datetime.now()#.strftime("%H:%M:%S.%f")
		s.send('TEST')
		timer_send2=datetime.now()#.strftime("%H:%M:%S.%f")
		print '1st TEST SENT AT', timer_send1
		print '2nd TEST SENT AT', timer_send2
	except socket.error:
		print 'Cannot send data. Please check connection'
		sys.exit(1) 

	try:
		data1 = s.recv(1024)	#how DO I TIME IT OUT HERE????
		timer_recv1= datetime.now()#.strftime("%H:%M:%S.%f")
		print 'reccieved', data1, 'at time', timer_recv1
		data2 = s.recv(1024)	
		timer_recv2=datetime.now()#.strftime("%H:%M:%S.%f")
		print 'recieved', data2, 'at time', timer_recv2 
	#	while data:
	#		data = s.recv(1024)
	except socket.error, socket.timeout:
		print 'Could not recieve from server! Please check if socket was correctly given.'
		sys.exit(1)
	
	
	#print 'I have recieved', data, 'from the server, at time', timer_recv
	#i=i+1
	print 'The packet dispersion is', timer_recv2-timer_recv1
except Exception, e:
	alert(e)

print 'Connection to', hostname, 'was succesful. Statistics to follow'
#print 'Total round trip time is', timer_recv-timer_send1
#print s.recv(1024)
s.shutdown(socket.SHUT_RDWR)
s.close()

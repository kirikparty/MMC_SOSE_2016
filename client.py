#!/usr/bin/python
import socket, sys, datetime, IN, os
import matplotlib.pyplot as plt

def alert(msg):
	print "Please check the below exception."
	print >>sys.stderr, msg
	sys.exit(1)

target_host = sys.argv[1]
target_port = int(sys.argv[2])

#if hostname[0] == '1':
#	print 'PLease enter the hostname in INET Address form (eg: abc.def.ghi.com) and not in IP Address V4 form.'
#	sys.exit(1)
#elif hostname[0] == '2':
#	print 'Please enter the hostname in INET Address form (eg: abc.def.ghi.com and not in IP Address form)'
#	sys.exit(1)

buffer_size = input("Enter the buffer size in Bytes. Do not exceed the MTU 1500 bytes: ")
if buffer_size > 1500:
	print("No. of bytes exceeds MTU... Exiting program!")
	sys.exit(1)
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

except Exception, e:
	print 'Failed to create socket!'
	alert(e)
#try:
#	host = socket.gethostbyname(hostname)
#except Exception, e:
#	print 'There was an error resolving the host.'
#	alert(e)

#print 'The host', hostname, 'has been resolved as', host, ':', port
print 'Connecting to host now...'
if os.path.isfile("Results1.txt") == True:
	os.remove("Results1.txt")

log = open("Results1.txt", "w")
print >>log, "test"
list_rate = []

try:
	
#	s.connect((host, port))
	timer_start = datetime.datetime.now()
	s.settimeout(100.0)
	
	print 'Connection started at', timer_start
	try:
		s.sendto('TEST',(target_host,target_port))
	except Exception, e:
		print 'Cannot send test data. Please check connection.'
		alert(e)
	try:
		data0 = s.recvfrom(buffer_size)
		print 'recieved', data0, 'from Server.  Connection established. Sending packets now...'
	except socket.error, socket.timeout:
		print 'Unable to establish connection. Please check the port address. Exiting now..'
		sys.exit(1)
	
	for i in range (200):
		try:
			a = 'A'*(buffer_size)
			s.sendto(a, (target_host, target_port));
			timer_send1=datetime.datetime.now()
			b= 'B'*(buffer_size)
			s.sendto(b, (target_host, target_port))
			timer_send2=datetime.datetime.now()
			print >> log, '1st PACKET SENT AT', timer_send1
			print >> log, '2nd PACKET SENT AT', timer_send2
		except Exception, e:
			print  'Cannot send data. Please check connection'
			alert(e) 
	
		try:
			data1 = s.recvfrom(buffer_size)
			timer_recv1= datetime.datetime.now()
			print >> log, 'recieved 1st PACKET at time', timer_recv1
			data2 = s.recvfrom(buffer_size)	
			timer_recv2=datetime.datetime.now()
			print >> log, 'recieved 2nd PACKET at time', timer_recv2 
		except socket.error, socket.timeout:
			print 'Could not recieve from server! Please check if socket was correctly given.'
			sys.exit(1)
		dispersion_time=timer_recv2-timer_recv1
		print dispersion_time
		link_rate = (buffer_size*8)/(dispersion_time.microseconds/(float (1000000)))
		link_rate_kbps = link_rate/(float(1000))
		list_rate.append(link_rate_kbps)
		print >> log, 'Dispersion is %.3f milliseconds \n \r' %((dispersion_time.microseconds)/float(1000))
		print 'Link rate is %.3f Kbps' %(link_rate/(float(1000)))
except Exception, e:
	alert(e)


plt.plot(list_rate)
plt.ylabel('Link rate in kbps')
plt.show()
print 'Connection to', target_host, 'was succesful. Statistics printed in the Results1.txt file'
#s.shutdown(socket.SHUT_RDWR)
s.close()

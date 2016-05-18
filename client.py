#!/usr/bin/python

"""
This program gives us the distribution of the bottleneck link rates and tells us for the particcular packet size in bytes, which is the best link rate
System Requirements:
1.Linux OS (Code will not work in Windows OS)
2.Python 2.7 or above
3.Python libraries of socket, datetime, matplotlib and numpy are installed
4.Working internet connection :)
The log file generated is Results1.txt. it is in the same folder as the code. In case the program errors out, the log file can be checked.
USAGE: python client.py HOSTNAME PORT
HOSTNAME can either be like abc.def.ghi.com or in the form of IP V4 address. DO NOT USE IP V6 address!
KNOWN BUG: SOMETIMES IF IP ADDRESS IS ENTERED INSTEAD
"""




import socket, sys, time, datetime, IN, os
import matplotlib.pyplot as plt			#Used for plotting the histogram
import numpy as np				#Used for calculating mean and variance

def alert(msg):					#We define an alert message which will present the error or exception thrown by python in a more readable way
	print "Please check the below exception."
	print >>sys.stderr, msg
	sys.exit(1)


"""Here we assign the Command Line arguments to target_host and target_port"""
target_host = sys.argv[1]		
target_port = int(sys.argv[2])


buffer_size = input("Enter the buffer size in Bytes. Do not exceed the MTU 1400 bytes: ")
if buffer_size > 1400:							#If packet byte size is greater than 1473 bytes, the program will automatically fragment it. Hence we need to limit
	print("No. of bytes exceeds MTU... Exiting program!")
	sys.exit(1)
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)		#socket connection used for UDP packets

except Exception, e:
	print 'Failed to create socket!'
	alert(e)

print 'Connecting to host now...'					#Here we open a log file where all the send and recieve times will be stored, for debugging purposes
if os.path.isfile("Results1.txt") == True:
	os.remove("Results1.txt")

log = open("Results1.txt", "w")
print >>log, "test"
list_rate = []								#We define a list called list_rate which will store all the bottleneck link rates for each execution

try:
	

	timer_start = datetime.datetime.now()
	s.settimeout(1.0)						#If there is no activity for 1 second, the timer will time out and move to the next packet
	
	print 'Connection started at', timer_start

	try:
		s.sendto('TEST',(target_host,target_port))		
	except Exception, e:
		print 'Cannot send test data. Please check connection. Also check if correct hostname and port was provided.'
		alert(e)
	try:
		data0 = s.recvfrom(buffer_size)
		print 'recieved', data0, 'from Server. Sending measurement packets now. \n Please wait for results. Logs are stored in Results1.txt generated in the same folder'
	except socket.error, socket.timeout:
		print 'Unable to establish connection. Please check the port address. Exiting now..'
		sys.exit(1)
#In python if we multiply a string or a character with a number, that string will be repeated those many times.Hence we multiply a single character with the packet size.
	a= 'A'*(buffer_size)
	b= 'B'*(buffer_size)

	for i in range (1000):		#We will do the measurements for the bottleneck link rate a 1000 times
		try:
			s.sendto(a, (target_host, target_port));
			s.sendto(b, (target_host, target_port))
		except Exception, e:
			print  'Cannot send data. Please check connection'
			alert(e) 
	
		try:
			data1 = s.recvfrom(buffer_size)
			timer_recv1= datetime.datetime.now()
			data2 = s.recvfrom(buffer_size)	
			timer_recv2=datetime.datetime.now()
			print >> log, 'recieved 1st PACKET at time', timer_recv1
			print >> log, 'recieved 2nd PACKET at time', timer_recv2 
		except socket.error, socket.timeout:
			print 'A Packet of the', i, 'th iteration was lost. Dropping this measurement'
			continue
		dispersion_time=timer_recv2-timer_recv1
		dispersion_float = dispersion_time.total_seconds()
		print >> log, dispersion_time
		if dispersion_float > 0.0:
			link_rate = ((buffer_size+28)*8)/(dispersion_time.microseconds/(float (1000000))) #We need to consider the 20 bytes for IP V4 header and 8 bytes for UDP packet header also
			link_rate_kbps = link_rate/(float(1000))
			dispersion_milli = dispersion_time.microseconds/float(1000)
		else:
			continue
		if link_rate_kbps < 100000 :		#Dropping values greater than 100 Mbps because they seem too unrealistic and mess with our readings
			list_rate.append(link_rate_kbps)
		else:
			continue
		print >> log, 'Dispersion is %.3f milliseconds \n \r' %((dispersion_time.microseconds)/float(1000))
		print >> log, 'Link rate is %.3f Kbps' %(link_rate/(float(1000)))
except Exception, e:
	alert(e)
s.close()			#Once our iterations are done, we properly tear down the socket connection

print " The mean is", np.mean(list_rate), "kbps"	#Calculating the mean bottleneck link rate for this particular packet size
print " The variance is ",np.var(list_rate)		#Calculating variance

"""We now use a dictionary to plot the histogram. The dictionary key will have the link rates in kbps and the dictionary values will store their frequqency"""
d = {x: list_rate.count(x) for x in list_rate}

plt.title("Probability Distribution of packet size %d bytes" % (buffer_size))

#Here we define another list linkProb which will store the probability of occurence of each of the link rate

linkProb = []

for j in d.values():
    j = float(j)/len(list_rate) #Dividing by the number of iterations gives us the probability
    linkProb.append(j)

plt.hist(d.keys(), weights=linkProb, bins=(max(list_rate)-min(list_rate))/50)
#We want to keep each bin size of about 50 kbps for 1000 measurements. Every 50 kbps probabilities will be averaged out
plt.xlabel('Link_Rates in Kbps')
plt.ylabel('Probability of link rates')
plt.show()			#Plot is shown, can be saved if required.

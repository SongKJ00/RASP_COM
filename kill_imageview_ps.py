import os
import time

while True:
	f = open('kill_flag.txt', 'r')
	line = f.readline()
	result = line.find('1')
	f.close()
	time.sleep(1)
	if result is not -1:
		f = open('kill_flag.txt', 'w')
		f.write('0')
		f.close()
		time.sleep(1)
		os.system('ps -ef | grep gpicview > killed_ps.txt')
		f = open('killed_ps.txt', 'r')
		while True:
			line = f.readline()
#			result = line.find('gpicview image.jpg')	
#			if result is not -1:
			if line[48:66] == 'gpicview image.jpg':
				pid = line[10:14]
				print('killed pid : %s' % pid)
				print('killed process : %s' % line[48:68])
				os.system('kill %s' % pid)
				break
			elif not line:
				break
		f.close()
		time.sleep(0.1)
	time.sleep(0.1)	

import RPi.GPIO as GPIO
import socket
import time
import os

os.system('ifconfig > ip.txt')
f = open("ip.txt", 'r')
while True:
	line = f.readline()
	result = line.find('inet addr:172.24.1.71')
	if result is not -1: 
		print("succeed")
		break

f.close()

PIR = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN)

HOST='172.24.1.1'
PORT=5007
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print('Connecting was succeed')

try:
	while True:
		detected = GPIO.input(PIR)
		#signal = s.recv(1024).decode('utf-8')
		if detected == True:
			s.send('T'.encode('utf-8'))
		else: 
			s.send('F'.encode('utf-8'))
		time.sleep(0.1)

except KeyboardInterrupt:
	s.close()
	GPIO.cleanup()

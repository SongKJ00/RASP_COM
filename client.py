import RPi.GPIO as GPIO
import socket
import time
import os

blue = 13
green = 26 
red = 19
PIR = 22 
sw = 9

GPIO.setmode(GPIO.BCM)
GPIO.setup(sw, GPIO.IN)
GPIO.setup(PIR, GPIO.IN)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)

#while True:
#	sw_on = GPIO.input(sw)
#	if sw_on == True:
#		break
#	time.sleep(0.1)

GPIO.output(red, True)
GPIO.output(blue, False)
GPIO.output(green, False)

while True:
	os.system('ifconfig > ip.txt')
	f = open('ip.txt', 'r')
	while True:
		line = f.readline()
		result = line.find('inet addr:172.24.1.71')
		if result is not -1:
			break
		elif not line:
			break
	f.close()
	time.sleep(0.01)
	if result is not -1: 	#서버 접속 성공
		print("ip connecting was succeed")
		break


HOST='172.24.1.1'
PORT=5007
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print('socket connecting was succeed')	#소켓 연결 성공

GPIO.output(green, True)
GPIO.output(blue, False)
GPIO.output(red, False)
time.sleep(5)
picture_flag = True

try:
	while True:
		GPIO.output(green, False)
		GPIO.output(blue, False)
		GPIO.output(red, False)
		try:
			detected = GPIO.input(PIR)
		#signal = s.recv(1024).decode('utf-8')
			if detected == True:
				print('motion detected')
				s.send('T'.encode('utf-8'))
				GPIO.output(blue, True)
				GPIO.output(red, False)
				GPIO.output(green, False)
				#take a picture only once
				if picture_flag == True:
					os.system('raspistill -vf -o image.jpg -t 1')
					#os.system('ps -ef > killed_ps.txt')
					f = open('kill_flag.txt', 'w')
					f.write('1')
					f.close()
					os.system('gpicview image.jpg')
					time.sleep(5)
					#picture_flag = False
#				while True:	#서버에서 종료 시그널이 올 때까지 데이터 송신 없이 기다림
#					signal = s.recv(1024).decode('utf-8')
#					if signal == 'E':
#						break
			else: 
				if picture_flag == False:
					picture_flag = True
				print('motion non-detected')
				s.send('F'.encode('utf-8'))
				GPIO.output(red, False)
				GPIO.output(blue,False)
				GPIO.output(green, True)
			time.sleep(0.1)
			
#if GPIO.input(sw) == False:
#				GPIO.output(red, True)
#				GPIO.output(blue, True)
#				GPIO.output(green, False)
		except IOError:
			pass

except KeyboardInterrupt:
	f.close()
	s.close()
	GPIO.cleanup()

except:
	for i in range(0, 10):
		if i%2 == 0:
			GPIO.output(red, True)
			GPIO.output(blue, False)
			GPIO.output(green, False)
		else:
			GPIO.output(red, False)
			GPIO.output(red, False)
			GPIO.output(red, False)
		time.sleep(0.3)
	f.close()
	s.close()
	GPIO.cleanup()



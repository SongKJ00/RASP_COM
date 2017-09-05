import RPi.GPIO as GPIO
import socket
import time

red = 26
blue = 19
green = 13
buzzer = 4
sw = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(sw, GPIO.IN)

GPIO.output(green, True) #초록색 소등
GPIO.output(buzzer, True)

print('Server on')
for led in range(0, 4):
	GPIO.output(red, False)
	GPIO.output(blue, True)
	time.sleep(0.5)
	GPIO.output(red, True)
	GPIO.output(blue, False)
	time.sleep(0.5)

#기본적으로 led 끔
GPIO.output(red, False)	#연결 될 때까지 대기
GPIO.output(blue, True)
GPIO.output(green, True)

HOST=''
PORT=5007
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)
GPIO.output(green, False)

try:
	while True:
		GPIO.output(buzzer, True)
		GPIO.output(green, False)
		data = conn.recv(1024).decode('utf-8')
		if data == 'T':
			GPIO.output(green, True)
			print("motion detected")
			for led_on in range(0, 15):
				if led_on%2 == 0:
					GPIO.output(red, True)
					GPIO.output(blue, False)
				else:
					GPIO.output(red, False)
					GPIO.output(blue, True)
				for buzzer_on in range(0, 100):
					GPIO.output(buzzer, True)
					time.sleep(0.001)
					GPIO.output(buzzer, False)
					time.sleep(0.001)
			#알림 후 led 끄기
			GPIO.output(red, True)
			GPIO.output(blue, True)

except KeyboardInterrupt:
	conn.close()
	GPIO.cleanup()

except:
	for i in range(0, 10):
		if i%2 == 0:
			GPIO.output(red, False)
			GPIO.output(blue, False)
			GPIO.output(green, False)
		else:
			GPIO.output(red, True)
			GPIO.output(blue, False)
			GPIO.output(green, False)
		time.sleep(0.3)
	conn.close()
	GPIO.cleanup()

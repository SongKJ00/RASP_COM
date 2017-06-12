import RPi.GPIO as GPIO
import socket
import time

red = 14
blue = 15
buzzer = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(red, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

HOST=''
PORT=5007
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

try:
	while True:
		data = conn.recv(1024).decode('utf-8')
		if data == 'T':
			print("motion detected")
			for i in range(0, 20):
				if i%2 == 0:
					GPIO.output(red, True)
					GPIO.output(blue, False)
				else:
					GPIO.output(red, False)
					GPIO.output(blue, True)
				for j in range(0, 100):
					GPIO.output(buzzer, True)
					time.sleep(0.001)
					GPIO.output(buzzer, False)
					time.sleep(0.001)
			#conn.send('E'.encode('utf-8'))

except KeyboardInterrupt:
	conn.close()
	GPIO.cleanup()

except Exception:
	conn.close()
	GPIO.cleanup()

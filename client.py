import socket

HOST='172.24.1.1'
PORT=5007
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print('Send data to server')
s.send('Y'.encode('utf-8'))
s.close()

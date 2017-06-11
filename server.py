import socket

HOST=''
PORT=5007
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

data = conn.recv(1024)
print('The received data is ', data.decode('utf-8'))
conn.close()

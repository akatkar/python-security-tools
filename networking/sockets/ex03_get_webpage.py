import socket

s = socket.socket()
s.connect(('data.pr4e.org',80))

cmd = 'GET http://data.pr4e.org/romeo.txt HTTP/1.0\r\n\r\n'.encode()
s.send(cmd)

while True:
    data = s.recv(512)
    if len(data) < 1:
        break
    print(data.decode())

s.close()

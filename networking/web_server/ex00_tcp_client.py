import socket

s = socket.socket()
host = socket.gethostname()
port = 9999

s.connect((host,port))
print('Server will be sending back the text which you send\n')
while True:
    text = input('send data:')
    if text.lower() in ['q', 'quit']:
        break
    s.send(text.encode())
    print(s.recv(1024).decode())

s.close()

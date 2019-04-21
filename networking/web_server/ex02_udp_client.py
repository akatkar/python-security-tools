import socket

address = ('localhost', 8888)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('Server will be sending back the text which you send as uppercase\n')
while True:
    data = input('>>> send data: ')
    if data in ['q', 'quit']:
        break
    sock.sendto(data.encode(), address)
    data = sock.recv(1024).decode()
    print('received:', data)

print(data)
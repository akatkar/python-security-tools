import socket

s = socket.socket()

host = socket.gethostname()
port = 12345

s.bind(('',port))
s.listen(5)

print("server is running...")
while True:
    client, address = s.accept()

    print("Got connection from ",address)
    client.send("Thank you from connecting".encode())
    client.close()


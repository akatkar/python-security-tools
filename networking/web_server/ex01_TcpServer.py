import socketserver


class EchoHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('Got connection from ', self.client_address)

        while True:
            data = self.request.recv(1024)
            if len(data) == 0:
                break
            print('client sent this:', data.decode())
            self.request.send(data)
        print('client left')


def main():
    address = ('0.0.0.0', 9999)
    server = socketserver.TCPServer(address, EchoHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()

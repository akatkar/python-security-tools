import socketserver


class UDPEchoHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request[0].strip().decode()
        socket = self.request[1]
        print(f'{self.client_address[0]} wrote: {data}')

        socket.sendto(data[::-1].encode(), self.client_address)


def main():
    address = ('localhost', 8888)
    server = socketserver.UDPServer(address, UDPEchoHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()




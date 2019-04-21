import socketserver
from http import server


def main():
    address = ('', 10001)
    http_server = socketserver.TCPServer(address, server.SimpleHTTPRequestHandler)
    http_server.serve_forever()

if __name__ == '__main__':
    main()
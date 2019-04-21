import socketserver
import http.server


class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/admin':
            # Construct a server response.
            self.send_response(200)
            self.end_headers()
            self.wfile.write('admin page\n\n'.encode())
            self.wfile.write(str(self.headers).encode())
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)


def main():
    address = ('', 10001)
    http_server = socketserver.TCPServer(address, HttpRequestHandler)
    http_server.serve_forever()

if __name__ == '__main__':
    main()

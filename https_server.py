#! /usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import sys
import ssl

COLOR = "\033[1;32m"
RESET_COLOR = "\033[00m"

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_log(self, method):
        try:
            content_length = self.headers['Content-Length']
            content_length = 0 if (content_length is None) else int(content_length)
            post_data = self.rfile.read(content_length)
            logging.info(COLOR + method + " request,\n" + RESET_COLOR + "Path: %s\nHeaders:\n%sBody:\n%s\n",
                         str(self.path), str(self.headers), post_data.decode('utf-8'))
            self._set_response()
            self.wfile.write((method + " request for {}".format(self.path)).encode('utf-8'))
        except Exception as e:
            # log the exception message
            logging.exception("An error occurred while processing the request: %s", e)
            # send a 500 Internal Server Error response to the client
            self.send_response(500)
            self.end_headers()
            self.wfile.write(("An error occurred while processing the request: {}".format(e)).encode('utf-8'))
        
    def do_GET(self):
        self.do_log("GET")

    def do_POST(self):
        self.do_log("POST")

    def do_PUT(self):
        self.do_log("PUT")

    def do_DELETE(self):
        self.do_log("DELETE")

def run(address, port, cert, key, server_class=HTTPServer, handler_class=S):
    logging.basicConfig(level=logging.INFO)
    server_address = (address, port)
    httpd = server_class(server_address, handler_class)

    # Create an SSL context and configure it
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert, keyfile=key)

    # Wrap the socket using the SSL context
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':                                                                                                                          
    if len(sys.argv) != 5:                                                                                                                          
        print("Usage:\n" + sys.argv[0] + " [address] [port] [cert] [key]")                                                                          
        sys.exit(1)                                                                                                                                 
                                                                                                                                                    
    run(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])  

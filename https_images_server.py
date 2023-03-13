#! /usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import sys
import ssl
import os
import subprocess

COLOR = "\033[1;32m"
RESET_COLOR = "\033[00m"

def load_js_file(filename):
    with open(filename, "r") as f:
        js_code = f.read()
    return "<script>" + js_code + "</script>"

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
        if self.path.startswith("/image/"):
            #logging.info('Path starts with /images/')
            # Extract the requested image filename
            image_filename = self.path[7:]
            js_code = load_js_file("./spoof/js/fingerprintjs.js")

            # Serve the requested image on an HTML page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(('<html><body>'+ js_code).encode())
            self.wfile.write('<img src="/images/{}" style="max-height: 100%;">'.format(image_filename).encode())
            self.wfile.write('</body></html>'.encode())

        elif self.path.startswith("/images/"):
            # Extract the requested image filename
            image_filename = self.path[8:]
            # Check if the requested image exists
            if not os.path.isfile('./images/' + image_filename):
                #logging.info('file does not exist so run imagemagick command')
                # The requested image does not exist, create it using ImageMagick
                subprocess.run(["./spoof/iMessage_1.sh", image_filename])

            #Serve the requested image
            with open('./images/' + image_filename, "rb") as f:
                #logging.info('Serving up file')
                image_data = f.read()
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                self.wfile.write(image_data)

        else:
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

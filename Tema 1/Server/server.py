import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

from api_all import start_all_api
import threading

IP = '127.0.0.1'
PORT = 8000

INTERFACE = '<div class="navbar"> ' \
            '<h1 class="logo">Cloud Tema 1</h1> ' \
            '</div>' \
            '<ul class="content"></ul>' \
            '<input class="picker" type="number" name="points" step="1" min="1" max="250" value="1">' \
            '<button type="button" class="request"><span> Start ! </span></button>'\
            '<button type="button" class="log"><span> Logs </span></button>'

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/interface':
            interface(self)
        if self.path == '/metrics':
            metrics(self)
        if self.path == '/testing':
            t = threading.Thread(target=testing(self))
            t.start()
        return
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH,OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        raw_data = re.findall(r'\d+',post_data.decode("utf-8"))
        print("Requested: " + raw_data[0] + " movies")
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        st = start_all_api(int(raw_data[0]))
        json_string = json.dumps(st)
        byt = json_string.encode()
        self.wfile.write(byt)
        print("Sending to client..[DONE]")
        return

def interface(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.send_header('Access-Control-Allow-Origin', '*')
    self.end_headers()
    # Trimite mesajul HTML
    st = INTERFACE
    byt = st.encode()
    self.wfile.write(byt)

def metrics(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.send_header('Access-Control-Allow-Origin', '*')
    self.end_headers()
    file = open("log.txt", "r")
    st = "<p style='white-space:pre-wrap;'>"+ file.read() +"</p>"
    byt = st.encode()
    self.wfile.write(byt)
    pass

def testing(self):
    self.send_response(200)
    self.send_header('Access-Control-Allow-Origin', '*')
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    st = start_all_api(5)
    json_string = json.dumps(st)
    byt = json_string.encode()
    self.wfile.write(byt)
    print("Sending to client..[DONE]")
    pass

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Gestionare cereri într-un fir separat."""

def run():
    server_address = (IP, PORT)
    httpd = ThreadedHTTPServer(server_address, myHandler)
    httpd.serve_forever()

run()
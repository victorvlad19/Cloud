import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

import simplejson as simplejson

import Get as get
import Post as post
import Put as put
import Delete as delete
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

IP = '127.0.0.1'
PORT = 8000

# Handler Http Request
class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if len(PurePosixPath(unquote(urlparse(self.path).path)).parts)>2:
                print(PurePosixPath(unquote(urlparse(self.path).path)).parts[2])
            if self.path == '/':
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("<body><p>Hello :) </p>".encode(encoding='utf_8'))
            if self.path == '/music':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(get.get_all_music().encode(encoding='utf_8'))
            taken_get = ['title', 'artist', 'year']
            if len(PurePosixPath(unquote(urlparse(self.path).path)).parts) > 2:
                if PurePosixPath(unquote(urlparse(self.path).path)).parts[2] not in taken_get:
                    if (get.get_specific_music( PurePosixPath(unquote(urlparse(self.path).path)).parts[2] ) != "Nil"):
                        print("Here")
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write( (get.get_specific_music( PurePosixPath(unquote(urlparse(self.path).path)).parts[2]) )
                                         .encode(encoding='utf_8'))
                    else:
                        print("NONE")
                        self.send_error(404, 'File Not Found: %s' % self.path)
            if self.path == '/music/title':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(get.get_title_music().encode(encoding='utf_8'))
            if self.path == '/music/artist':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(get.get_artist_music().encode(encoding='utf_8'))
                self.wfile.write("<body><p>Artist.</p>".encode(encoding='utf_8'))
            if self.path == '/music/year':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(get.get_year_music().encode(encoding='utf_8'))
        except:
            self.send_error(404, 'File Not Found: %s' % self.path)
    def do_POST(self):
        # Colectie de resurse
        if self.path == '/music':
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = simplejson.loads(self.data_string)
            if post.check_colection_music(data) != "409":
                if post.post_collection_music(data) == "OK":
                    self.send_response(201)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write("File created.".encode(encoding='utf_8'))
                else:
                    self.send_error(500, 'Internal Server Error %s' % self.path)
            else:
                self.send_error(409, 'Conflict: %s' % self.path)
        # O singura resursa
        if len(PurePosixPath(unquote(urlparse(self.path).path)).parts) > 2:
            if (post.check_specific_music(PurePosixPath(unquote(urlparse(self.path).path)).parts[2]) != "409"):
                self.data_string = self.rfile.read(int(self.headers['Content-Length']))
                data = simplejson.loads(self.data_string)
                if post.post_specific_music(PurePosixPath(unquote(urlparse(self.path).path)).parts[2],data)  == "OK":
                    self.send_response(201)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write("File created.".encode(encoding='utf_8'))
                else:
                    self.send_error(500, 'Internal Server Error %s' % self.path)
            else:
                self.send_error(409, 'Conflict: %s' % self.path)
    def do_PUT(self):
        # Colectie de resurse
        if self.path == '/music':
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = simplejson.loads(self.data_string)
            if put.check_colection_music(data) != "404":
                if put.put_collection_music(data) == "OK":
                    self.send_response(201)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write("File updated.".encode(encoding='utf_8'))
                else:
                    self.send_error(500, 'Internal Server Error %s' % self.path)
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)
        if len(PurePosixPath(unquote(urlparse(self.path).path)).parts) > 2:
            if (put.check_specific_music(PurePosixPath(unquote(urlparse(self.path).path)).parts[2]) != "404"):
                self.data_string = self.rfile.read(int(self.headers['Content-Length']))
                data = simplejson.loads(self.data_string)
                if put.put_specific_music(PurePosixPath(unquote(urlparse(self.path).path)).parts[2], data) == "OK":
                    self.send_response(201)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write("File updated.".encode(encoding='utf_8'))
                else:
                    self.send_error(500, 'Internal Server Error %s' % self.path)
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)
    def do_DELETE(self):
        # Colectie de resurse
        if self.path == '/music':
            self.data_string = self.rfile.read(int(self.headers['Content-Length']))
            data = simplejson.loads(self.data_string)
            print(data)
            if delete.check_colection_music(data) != "404":
                if delete.delete_collection_music(data) == "OK":
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write("Files deleted.".encode(encoding='utf_8'))
                else:
                    self.send_error(500, 'Internal Server Error %s' % self.path)
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)
        if len(PurePosixPath(unquote(urlparse(self.path).path)).parts) > 2:
            if (delete.check_specific_music(PurePosixPath(unquote(urlparse(self.path).path)).parts[2]) != "404"):
                if delete.delete_specific_music(PurePosixPath(unquote(urlparse(self.path).path)).parts[2]) == "OK":
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write("Files deleted.".encode(encoding='utf_8'))
                else:
                    self.send_error(500, 'Internal Server Error %s' % self.path)
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Gestionare cereri într-un fir separat."""

def run():
    server_address = (IP, PORT)
    httpd = ThreadedHTTPServer(server_address, myHandler)
    print(time.asctime(), 'Server-ul Porneste - %s:%s' % (IP, PORT))
    httpd.serve_forever()

run()
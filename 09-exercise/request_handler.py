from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import socket.timeout

def make_forward_handler(upstream_url):
    class ForwardHTTPRequestHandler(BaseHTTPRequestHandler):

        def __init__(self, *args, **kwargs):
            super(ForwardHTTPRequestHandler, self).__init__(*args, **kwargs)

        def do_GET(self):

            req = Request('http://' + upstream_url + self.path)
            for key in self.headers:
                print(key)
                print(self.headers[key])
                req.add_header(key, self.headers[key])

            try:
                res = urlopen(req, timeout=1)
            except (HTTPError, URLError) as error:
                print(e)
            except socket.timeout:
                print('timeout')
            else:
                print(res.getcode())
                print(res.info())



        def do_POST(self):
            print(self)

    return ForwardHTTPRequestHandler

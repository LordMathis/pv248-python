from sys import argv
import urllib
import os
from socketserver import ThreadingMixIn
from http.server import HTTPServer
from http.server import CGIHTTPRequestHandler

def make_cgi_handler(port, dir):
    class Handler(CGIHTTPRequestHandler):

        def send_file(self, file_path):
            pass

        def do_GET(self):

            parsed_url = urllib.parse.urlparse(self.path)
            req_params = parsed_url.query
            req_path = os.path.join(__file__, dir, parsed_url.path[1:])

            if os.path.isfile(req_path):
                if req_path.endswith('.cgi'):
                    self.cgi_info = dir, parsed_url.path[1:] + '?' + req_params
                    self.run_cgi()
                else:
                    with open(req_path) as file:
                        self.send_file(req_path)
            else:
                self.send_error(404, 'Not Found')

        def do_POST(self):
            req_content_legth = int(self.headers['Content-Length'])
            req_body = self.rfile.read(req_content_legth).decode('utf-8')

            if os.path.isfile(req_path):
                if req_path.endswith('.cgi'):
                    self.cgi_info = dir, parsed_url.path[1:] + '?' + req_params
                    self.run_cgi()
                else:
                    with open(req_path) as file:
                        self.send_file(req_path)
            else:
                self.send_error(404, 'Not Found')

    return Handler

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    port = int(argv[1])
    dir = argv[2]

    Handler = make_cgi_handler(port, dir)

    httpd = ThreadedHTTPServer(('', port), Handler)
    httpd.serve_forever()

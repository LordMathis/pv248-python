from sys import argv
import urllib
import os
from socketserver import ThreadingMixIn
from http.server import HTTPServer
from http.server import CGIHTTPRequestHandler

def make_cgi_handler(port, dir):

    class Handler(CGIHTTPRequestHandler):

        cgi_directories = [os.path.normpath(os.path.join(os.getcwd(), dir))]

        def send_file(self, file_path):
            with open(file_path, 'rb') as f:
                size = os.path.getsize(file_path)

                data = f.read()

                self.send_response(200)
                self.send_header('Content-Length', str(size))
                self.end_headers()
                self.wfile.write(data)


        def run(self, path, params):
            print('running cgi script')
            print(path)
            self.cgi_info = os.path.relpath(dir), path + '?' + params
            self.run_cgi()

        def get_path(self, path):
            return os.path.normpath(os.path.join(os.getcwd(), dir, path))

        def do_GET(self):

            parsed_url = urllib.parse.urlparse(self.path)
            req_params = parsed_url.query
            req_path = self.get_path(parsed_url.path[1:])

            if os.path.isfile(req_path):
                if req_path.endswith('.cgi'):
                    self.run(parsed_url.path[1:], req_params)
                else:
                    self.send_file(req_path)
            else:
                self.send_error(403, 'Forbidden')

        def do_POST(self):
            req_content_legth = int(self.headers['Content-Length'])
            req_body = self.rfile.read(req_content_legth).decode('utf-8')

            parsed_url = urllib.parse.urlparse(self.path)
            req_params = parsed_url.query
            req_path = self.get_path(parsed_url.path[1:])

            if os.path.isfile(req_path):
                if req_path.endswith('.cgi'):
                    self.run(parsed_url.path[1:], req_params)
                else:
                    self.send_file(req_path)
            else:
                self.send_error(403, 'Forbidden')

    return Handler

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    port = int(argv[1])
    dir = argv[2]

    Handler = make_cgi_handler(port, dir)

    httpd = ThreadedHTTPServer(('', port), Handler)
    httpd.serve_forever()

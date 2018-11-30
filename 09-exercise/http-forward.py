from sys import argv
from http.server import HTTPServer
import request_handler

if __name__ == '__main__':
    port = int(argv[1])
    upstream = argv[2]

    if (not upstream.startswith('http://')
        and not upstream.startswith('https://')):
        upstream = 'http://' + upstream


    Handler = request_handler.make_forward_handler(upstream)

    httpd = HTTPServer(('', port), Handler)
    httpd.serve_forever()

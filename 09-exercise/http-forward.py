from sys import argv
from http.server import HTTPServer
import request_handler
import ssl

if __name__ == '__main__':
    port = int(argv[1])
    upstream = argv[2]

    Handler = request_handler.make_forward_handler(upstream)

    httpd = HTTPServer(('', port), Handler)
    httpd.serve_forever()

import os
import json
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def make_forward_handler(upstream_url):
    class ForwardHTTPRequestHandler(BaseHTTPRequestHandler):

        def __init__(self, *args, **kwargs):
            super(ForwardHTTPRequestHandler, self).__init__(*args, **kwargs)

        def send_request(self, url, headers, data=None, timeout=1, method='GET'):

            res_json = {}

            req = Request(url, headers=headers, data=data, method=method)

            try:
                res = urlopen(req, timeout=timeout)
            except HTTPError as http_error:
                res_json['code'] = http_error.code
                res_json['headers'] = dict(http_error.headers)
            except URLError as url_error:
                print(url_error)
                raise
            except socket.timeout:
                res_json['code'] = 'timeout'
            else:
                res_json['code'] = res.getcode()
                res_json['headers'] = dict(res.getheaders())

                res_data = res.read()

                try:
                    res_data_json = json.loads(res_data)
                except:
                    res_json['content'] = str(res_data)
                else:
                    res_json['json'] = res_data_json

            return res_json

        def do_GET(self):

            url = upstream_url + self.path
            headers = {}
            for key in self.headers:
                headers[key] = self.headers[key]

            res_json = self.send_request(url, headers)

            res_content = bytes(json.dumps(res_json,
                                           indent=4,
                                           sort_keys=False,
                                           ensure_ascii=False), 'utf-8')

            self.send_response(200, 'OK')
            self.send_header('Connection', 'close')
            self.send_header('Content-Type', 'text/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(res_content)

        def do_POST(self):

            req_content_legth = int(self.headers['Content-Length'])
            req_body = self.rfile.read(req_content_legth).decode('utf-8')
            res_json = {}

            try:
                req = json.loads(req_body)
            except:
                res_json['code'] = 'invalid json'
            else:
                type = req['type'] if 'type' in req else 'GET'

                if (req['url'] is None or
                    (type == 'POST' and
                     req['content'] is None)):
                    res_json['code'] = 'invalid json'

                else:
                    headers = req['headers'] if 'headers' in req else {}

                    if type == 'POST':

                        headers['Accept-Encoding'] = 'identity'
                        data = urlencode(req['content']).encode('utf-8')


                    req_timeout = int(req['timeout']) if req['timeout'] else 1
                    res_json = self.send_request(req['url'], headers, data, req_timeout, type)

            res_content = bytes(json.dumps(res_json,
                                           indent=4,
                                           sort_keys=False,
                                           ensure_ascii=False), 'utf-8')

            self.send_response(200, 'OK')
            self.send_header('Connection', 'close')
            self.send_header('Content-Type', 'text/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(res_content)


    return ForwardHTTPRequestHandler

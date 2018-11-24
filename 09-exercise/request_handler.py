import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from socket import timeout

def make_forward_handler(upstream_url):
    class ForwardHTTPRequestHandler(BaseHTTPRequestHandler):

        def __init__(self, *args, **kwargs):
            super(ForwardHTTPRequestHandler, self).__init__(*args, **kwargs)

        def do_GET(self):

            res_json = {}

            req = Request('http://' + upstream_url + self.path)
            for key in self.headers:
                if key == 'Host' and upstream_url not in self.headers[key]:
                    req.add_header(key, upstream_url)
                else:
                    req.add_header(key, self.headers[key])

            try:
                res = urlopen(req, timeout=1)
            except (HTTPError, URLError) as error:
                print(e)
            except timeout:
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
            req_body = self.rfile.read(req_content_legth)
            res_json = {}

            try:
                req = json.loads(req_body)
            except:
                res_json['code'] = 'invalid json'
            else:
                if (req['url'] is None or
                    (req['type'] == 'POST' and
                     req['content'] is None)):
                    res_json['code'] = 'invalid json'
                else:
                    if req['type'] == 'POST':
                        request = Request(req['url'],
                                          data=req['content'],
                                          headers=req['headers'])
                    else:
                        request = Request(req['url'],
                                          headers=req['headers'])

                    req_timeout = int(req['timeout']) if req['timeout'] else 1

                    try:
                        res = urlopen(request, timeout=req_timeout)
                    except (HTTPError, URLError) as error:
                        print(e)
                    except timeout:
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

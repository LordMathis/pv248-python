from sys import argv
import urllib
from game import Game
import json
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler

games = {}
max_id = 0

class TicTacToeHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super(TicTacToeHandler, self).__init__(*args, **kwargs)

    def do_GET(self):

        global games
        global max_id

        parsed_url = urllib.parse.urlparse(self.path)
        req_params = urllib.parse.parse_qs(parsed_url.query)
        req_path = parsed_url.path.strip('/')

        res_json = {}

        if req_path == 'start':

            name = req_params['name'][0] if 'name' in req_params else ''

            game = Game(name)
            games[max_id] = game
            res_json['status'] = 'ok'
            res_json['message'] = 'ok'
            res_json['id'] = max_id

            max_id += 1

        else:

            if req_path == 'list':
                game_list = []

                for game_id in games:
                    game = games[game_id]

                    if not game.full:
                        game_list.append({
                            'id': game_id,
                            'name': game.name
                        });

                res_json['games'] = game_list

            elif 'game' not in req_params:

                self.send_error(400, 'Bad Request')

            elif int(req_params['game'][0]) not in games:

                res_json['status'] = 'bad'
                res_json['message'] = 'Game with id {} does not exists'.format(req_params['game'][0])

            elif req_path == 'status':

                game_id = int(req_params['game'][0])
                game = games[game_id]

                if game.status is None:
                    res_json['board'] = game.board
                    res_json['full'] = game.full
                    res_json['next'] = game.next
                else:
                    res_json['board'] = game.board
                    res_json['winner'] = game.status

            elif req_path == 'play':

                game_id = int(req_params['game'][0])
                player = int(req_params['player'][0])
                x = int(req_params['x'][0])
                y = int(req_params['y'][0])

                game = games[game_id]
                status, message = game.play(player, x, y)

                res_json['status'] = status
                res_json['message'] = message
                res_json['board'] = game.board

            elif req_path == 'join':

                game_id = int(req_params['game'][0])

                if games[game_id].full:
                    res_json['status'] = 'bad'
                    res_json['message'] = 'Game with id {} is already full'.format(game_id)

                else:
                    games[game_id].full = True
                    res_json = {
                        'status': 'ok',
                        'message': 'ok',
                        'id': game_id
                    }

            else:
                self.send_error(404, 'Not Found')

        res_content = bytes(json.dumps(res_json,
                                       indent=4,
                                       sort_keys=False,
                                       ensure_ascii=False), 'utf-8')

        self.send_response(200, 'OK')
        self.send_header('Connection', 'close')
        self.send_header('Content-Type', 'text/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(res_content)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    port = int(argv[1])

    httpd = ThreadedHTTPServer(('', port), TicTacToeHandler)
    httpd.serve_forever()

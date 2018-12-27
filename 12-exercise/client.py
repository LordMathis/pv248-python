from sys import argv, stdin
from urllib.request import Request, urlopen, urlretrieve
from urllib.parse import urlencode, urljoin
from time import sleep
import json

def send_request(url, path, query):

    encoded_query = urlencode(query)
    req_url = urljoin(url, path)


    if encoded_query:
        req_url = req_url + '?' + encoded_query

    req = Request(req_url)

    try:
        res = urlopen(req)
    except:
        print('Something went wrong')
    else:
        try:
            res_json = json.loads(res.read())
        except:
            print('Response is not a valid json')
        else:
            return res_json

def play_game(url, game_id, player):

    full = False

    while True:
        res = send_request(url, 'status', {'game': game_id})
        # print(res)

        if not full:
            full = res['full']

        if 'winner' in res:
            print_board(res['board'])
            if res['winner'] == 0:
                print("draw")
            else:
                if res['winner'] == player:
                    print('you win')
                else:
                    print('you lose')
            return

        elif full and res['next'] == player:
            print_board(res['board'])
            print('your turn ({})'.format('x' if player == 1 else 'o'))

            user_input = stdin.readline().rstrip('\n').strip()
            if len(user_input.split()) != 2:
                print("invalid input")
                continue

            x, y = tuple(user_input.split())

            query = {
                'game': game_id,
                'player': player,
                'x': x,
                'y': y
            }

            play_res = send_request(url, 'play', query)

            if play_res['status'] == 'bad':
                print(play_res['message'])
            else:
                print_board(play_res['board'])
                print("waiting for other player")

        else:
            sleep(1)



def print_board(board):

    symbols = ['_', 'X', 'O']

    for i, row in enumerate(board):
        row_str = ''
        for cell in row:
            row_str += symbols[cell]
        print(row_str)


if __name__ == '__main__':

    play = True
    url = argv[1]
    port = argv[2]

    if (not url.startswith('http://')
        and not url.startswith('https://')):
        url = 'http://' + url

    url = url + ':' + port

    while play:
        game_list = send_request(url, 'list', {})

        game_ids = []

        if len(game_list['games']) > 0:
            print('Available games:')
            for game in game_list['games']:
                print('{} {}'.format(game['id'], game['name']))
                game_ids.append(int(game['id']))
                print('Type game id to join or "new game_name" to start new game')

        else:
            print('There are no game available on the server. Type "new game_name" to start new game')

        user_input = stdin.readline().rstrip('\n')

        if user_input.startswith('new'):
            name = user_input[3:].strip()
            path = 'start'
            if name:
                query = {
                    'name': name
                }
            else:
                query = {}

            res = send_request(url, path, query)

            if res['status'] == 'bad':
                print(res['message'])
            else:
                print('Game started, waiting for someone to join...')
                play_game(url, res['id'], 1)

        elif int(user_input) in game_ids:

            path = 'join'
            query = {
                'game': int(user_input)
            }

            res = send_request(url, path, query)

            if res['status'] == 'bad':
                print(res['message'])
            else:
                print('Joined game {}, waiting for other player...'.format(int(user_input)))
                play_game(url, res['id'], 2)

        else:
            print('Unknown game id: {}'.format(user_input))

        print('Play again? [Y|n]')
        user_input = stdin.readline().rstrip('\n')

        if user_input not in ['', 'y', 'Y']:
            play = False

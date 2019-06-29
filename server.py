import os
import random

import socketio
import eventlet

port = 5000

PLAYERS = {}

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={'/': {'content_type': 'text/html', 'filename': 'index.html'}})


def get_honorific():
    honorifics = [
        'great', 'emperor', 'child', 'jester', 'captain', 'fool', 'cunt', 'king', 'gay', 'queer', 'donkey'
        'faceless', 'queen', 'young', 'bold', 'timid', 'peasant', 'big man',
        'flaccid', 'giant', 'weak', 'poor', 'farmer', 'knight', 'animal', 'predator',
        'guardian', 'fork', 'bitch', 'pleb', 'brave', 'coward', 'legless', 'nugget'
    ]
    return f'the {honorifics[random.randrange(0, len(honorifics))]}'


def speak(msg):
    os.system(f'say {msg}')


def shutdown():
    if PLAYERS:
        speak(f'Death is inevitable. Killing {len(PLAYERS)} players.')
    else:
        speak('Server shutting down.')


class Player:

    def __init__(self, name, honorific):
        self.name = name
        self.honorific = honorific


@sio.event
def connect(sid, _):
    speak(f'New connection')


@sio.event
def disconnect(sid):
    if sid in PLAYERS:
        player = PLAYERS[sid]
        speak(f'Player {player.fullname} has died.')
        del PLAYERS[sid]
    assert sid not in PLAYERS

    player_list = [[player.name, player.honorific] for player in PLAYERS.values()]
    sio.emit('lobby', {'players': player_list})


@sio.on('hello')
def hello(sid, data):
    print('data:', data)
    print(sid)


@sio.on('intro')
def intro(sid, data):
    assert sid not in PLAYERS
    player = Player(data['name'], get_honorific())  # create player
    PLAYERS[sid] = player  # add to player dict
    player.fullname = f'{player.name} {player.honorific}'
    speak(f'New player: {player.name} - {player.honorific}.')

    player_list = [[player.name, player.honorific] for player in PLAYERS.values()]
    sio.emit('lobby', {'honorific': player.honorific, 'players': player_list})


@sio.on('start')
def start(sid):
    player_name = PLAYERS[sid]['name']
    speak(f'Player - {player_name} - is starting this bitch of a game.')
    sio.emit()


@sio.on('read_end')
def read_end():
    pass


def start_server():
    speak('Starting server')
    eventlet.wsgi.server(eventlet.listen(('', port)), app)

if __name__ == '__main__':
    start_server()
    shutdown()

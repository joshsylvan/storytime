import os
import time
import random

import socketio
import eventlet

port = 5000

PLAYERS = {}

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={'/': {'content_type': 'text/html', 'filename': 'index.html'}})

CURRENT_STORY = None


class Story:
    players = []

    def get_next(self):
        return self.next


class StoryNarration(Story):
    def __init__(self, name, data):
        self.name, self.data = name, data.split('. ')

    def emit(self):
        emit_narrator(self)


class StoryInput(Story):
    def __init__(self, name, data,):
        self.name, self.data = name, data.split('. ')
        self.next = None

    def emit(self):
        emit_input(self)


class StoryDecision(Story):
    def __init__(self, name, data):
        self.name, self.data = name, data
        self.left, self.right = None, None

    def get_next(self):
        return [next_story if len(next_story.players) > 0 else None for next_story in [self.left, self.right]]

    def get_name(self):
        pass

    def emit(self):
        emit_choice(self)


class Player:
    def __init__(self, name, honorific):
        self.name = name
        self.honorific = honorific
        self.has_responded = None
        self.responses = {}


def construct_story():
    """"""
    intro = StoryNarration('intro', 'You are in front of this mansion. What are you wearing?')
    disguise = StoryInput('disguise', 'What disguise are you wearing?')
    entering = StoryNarration('entering', 'You enter the mansion. People greet you and ask what gift you brought.')
    gift = StoryInput('gift', 'What gift did you bring?')
    thanks = StoryNarration('thanks', 'You may enter. You approach people, what do you say?')
    mingle = StoryInput('mingle', 'You approach some people, what do you say?')
    awkward = StoryNarration('awkward', 'You are weird. Leave. You need to find Hitler.')
    search = StoryDecision('search', {'question': 'Where do you go to find Hitler himself?', 'choices': ['Garden', 'Library']})

    garden = StoryInput('garden', 'What you drinking fam?')
    library = StoryInput('library', "What do you think of Hitler's painting?")

    search.left = garden
    search.right = library
    awkward.next = search
    mingle.next = awkward
    thanks.next = mingle
    gift.next = thanks
    entering.next = gift
    disguise.next = entering
    intro.next = disguise

    return intro


def advance_story():
    global CURRENT_STORY
    next_story = CURRENT_STORY.get_next()
    print(f'story: current={CURRENT_STORY.name}, next={next_story.name}')
    CURRENT_STORY = next_story
    CURRENT_STORY.emit()


def get_honorific():
    honorifics = [
        'great', 'emperor', 'child', 'jester', 'captain', 'fool', 'cunt', 'king', 'donkey', 'devil',
        'faceless', 'queen', 'young', 'bold', 'timid', 'peasant', 'big man', 'monster', 'maniac', 'flamboyant',
        'jockey', 'flaccid', 'giant', 'weak', 'poor', 'farmer', 'knight', 'animal', 'predator', 'strangled', 'drowned',
        'smelly', 'guardian', 'fork', 'bitch', 'pleb', 'brave', 'coward', 'legless', 'nugget', 'fallen', 'forsaken',
        'grey', 'fat', 'ugly', 'sad', 'zombie', 'grinch', 'deranged'
    ]
    return f'the {honorifics[random.randrange(0, len(honorifics))]}'


def speak(msg):
    sio.emit('speak', msg)


def shutdown():
    if PLAYERS:
        os.system(f'say "Death is inevitable. Killing {len(PLAYERS)} players."')
    else:
        os.system('say "Server shutting down."')


def emit_lobby(player):
    """Lobby"""
    player_list = [[player.name, player.honorific] for player in PLAYERS.values()]
    sio.emit('lobby', {'honorific': player.honorific, 'players': player_list})


def emit_narrator(story):
    """Narrator block without input."""
    sio.emit('narrator', story.data)


def emit_input(story):
    """Send input prompt and wait for all feedback. """
    print(f'emitting input {story.name}')
    sio.emit('input', {'question': story.data})


def emit_choice(story):
    """Send choice prompt and wait for all feedback"""
    print(f'emitting choice {story.name}')
    sio.emit('choice', story.data)


def check_all_players_done():
    """Update path and then give to narrator."""
    print('waiting for responses')
    total_players = len(PLAYERS)
    responses = 0

    for player in PLAYERS.values():
        if player.has_responded:
            responses += 1

    print(f'responses: {responses}')

    if responses == total_players:
        print('All players responded')
        for player in PLAYERS.values():
            player.has_responded = False
        advance_story()


@sio.event
def connect(sid, _):
    # speak(f'New connection')
    pass


@sio.event
def disconnect(sid):
    if sid in PLAYERS:
        player = PLAYERS[sid]
        speak(f'Player {player.fullname} brutally died.')
        del PLAYERS[sid]
        emit_lobby(player)
    assert sid not in PLAYERS


@sio.on('intro')
def intro(sid, data):
    assert sid not in PLAYERS
    player = Player(data['name'], get_honorific())  # create player
    PLAYERS[sid] = player  # add to player dict
    player.fullname = f'{player.name} {player.honorific}'
    speak(f'New player: {player.name} - {player.honorific}.')

    emit_lobby(player)


@sio.on('start')
def start(sid):
    global CURRENT_STORY
    player_name = PLAYERS[sid].name
    speak(f'Player - {player_name} - is starting this bitch of a game.')
    CURRENT_STORY = construct_story()
    emit_narrator(CURRENT_STORY)


@sio.on('read_end')
def read_end(sid):
    """End of narration spoken. Get next action."""
    advance_story()


@sio.on('next')
def next(sid, data):
    global CURRENT_STORY
    type, response = data['body']['type'], data['body']['data']
    player = PLAYERS[sid]
    print(f'next: player={player.name}, response={response}')
    player.has_responded = True
    player.responses[CURRENT_STORY.name] = response

    if isinstance(CURRENT_STORY, StoryDecision):
        if CURRENT_STORY.left.name == response:
            CURRENT_STORY.left.players.append(sid)
        else:
            CURRENT_STORY.right.players.append(sid)
    check_all_players_done()


def start_server():
    os.system('say "starting server"')
    eventlet.wsgi.server(eventlet.listen(('', port)), app)

if __name__ == '__main__':
    start_server()
    shutdown()

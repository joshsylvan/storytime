"""Receivers."""

from . import emitters, story
from .server_handler import sio

@sio.event
def connect(sid, _):
    # emitters.speak(f'New connection')
    print("new connection")

@sio.event
def disconnect(sid):
    players = story.PLAYERS
    if sid in players:
        player = players[sid]
        emitters.speak(f'Player {player.fullname} brutally died.')
        del players[sid]
        emitters.emit_lobby(player)
        print("local players:", players)
        print("global players:", story.PLAYERS)
    assert sid not in players


@sio.on('intro')
def intro(sid, data):
    print("intro")
    players = story.PLAYERS
    assert sid not in players
    player = story.Player(data['name'], story.get_honorific())  # create player
    players[sid] = player  # add to player dict
    player.fullname = f'{player.name} {player.honorific}'
    emitters.speak(f'New player: {player.name} - {player.honorific}.')

    emitters.emit_lobby(player)


@sio.on('start')
def start(sid):
    player_name = story.PLAYERS[sid].name
    emitters.speak(f'{player_name} - is starting the game.')
    story.start()
    story_text = story.get_story_text()
    emitters.emit_narrator(story_text)


@sio.on('read_end')
def read_end(sid):
    """End of narration spoken. Get next action."""
    story.advance_story()


@sio.on('next')
def next(sid, data):
    type, response = data['body']['type'], data['body']['data']
    player = story.PLAYERS[sid]
    print(f'next: player={player.name}, response={response}')
    player.has_responded = True
    response_name = f'response_{story.CURRENT_STORY.name}'
    setattr(player, response_name, response)

    if isinstance(story.CURRENT_STORY, story.StoryDecision):
        if story.CURRENT_STORY.left.name == response:
            story.CURRENT_STORY.left.players.append(sid)
        else:
            story.CURRENT_STORY.right.players.append(sid)
    story.check_all_players_done()

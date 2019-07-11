"""Emitters."""

from .server_handler import sio

def speak(message):
    """Make browser speak message."""
    sio.emit('speak', message)


def emit_lobby(player):
    """Lobby"""
    from .story import PLAYERS
    print("EMITTING LOBBY")
    player_list = [[player.name, player.honorific] for player in PLAYERS.values()]
    sio.emit('lobby', {'honorific': player.honorific, 'players': player_list})


def emit_narrator(text):
    """Narrator block without input."""
    sio.emit('narrator', text)


def emit_input(story):
    """Send input prompt and wait for all feedback. """
    print(f'emitting input {story.name}')
    sio.emit('input', {'question': story.data})


def emit_choice(story):
    """Send choice prompt and wait for all feedback"""
    print(f'emitting choice {story.name}')
    sio.emit('choice', story.data)

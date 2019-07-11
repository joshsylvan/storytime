import socketio
import eventlet
import jinja2

port = 5000

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={'/': {'content_type': 'text/html', 'filename': 'index.html'}})

def server_stop():
    from . import story
    if story.PLAYERS:
        print(f'Death is inevitable. Killing {len(story.PLAYERS)} players.')
    else:
        print('Server shutting down.')

from . import emitters, receivers

def server_start():
    print('Starting server')
    eventlet.wsgi.server(eventlet.listen(('', port)), app)

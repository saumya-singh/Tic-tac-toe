from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms
import json

app = Flask(__name__)
socketio = SocketIO(app)
players_connected = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/grid/')
def grid():
    return render_template('grid.html')


@socketio.on('join_player')
def value_changed(player_id):
    player = json.loads(player_id)
    username = player['username']
    room = player['id']
    join_room(room)
    if room not in players_connected:
        players_connected[room] = [request.sid]
        emit('user update', username + ' has entered the room.', room=room)
    elif len(players_connected) == 1:
        players_connected[room].append(request.sid)
        emit('users joined', [username + ' has entered the room.', room, players_connected[room]], room=room)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug = True)

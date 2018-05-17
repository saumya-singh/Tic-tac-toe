from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms
import json, random

app = Flask(__name__)
socketio = SocketIO(app)
players_connected = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/grid/')
def grid():
    return render_template('grid.html')


@socketio.on('join player')
def join_player(player_id):
    player = json.loads(player_id)
    username = player['username']
    room = player['id']
    join_room(room)
    if room not in players_connected:
        players_connected[room] = {username: request.sid}
        emit('user update', username + ' has entered the room.', room=room)
    elif len(players_connected) == 1:
        players_connected[room].update({username: request.sid})
        emit('users joined', [username + ' has joined the room.', room, players_connected[room]], room=room)


@socketio.on('select player')
def select_player(room_details):
    print("=================================", room_details)
    people = list(room_details[1].keys())
    print("==========people: ", people)
    player1 = random.choice(people)
    print("==========people111: ", type(player1))
    people.remove(player1)
    player2 = people.pop()
    print("==========people222: ", player2)
    player_dict = {"player1": player1, "player2": player2}
    emit('display', [player_dict, room_details[1], room_details], room=room_details[1])


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug = True)

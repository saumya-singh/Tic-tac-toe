from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms
from itertools import cycle
import json

app = Flask(__name__)
socketio = SocketIO(app)
players_connected = {}
myIterator = cycle(range(1, 3))


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('join player')
def join_player(player_id):
    player = json.loads(player_id)
    username = player['username']
    room = player['id']
    join_room(room)
    if room not in players_connected:
        print("one player added")
        players_connected[room] = {username: request.sid}
        emit('user update', username + ' has joined the room.', room=room)
    elif len(players_connected) == 1:
        print("second player added")
        players_connected[room].update({username: request.sid})
        emit('users joined', [username + ' has joined the room.', room, players_connected[room]], room=room)


@socketio.on('play game')
def play_game(details):
    active_player = next(myIterator)
    active_player_name = details[2]["player" + active_player]
    active_player_sid = details[1][active_player_name]
    sid_list = list(details[2].keys())
    sid_list.remove(active_player_sid)
    disable_player_sid = sid_list.pop()
    status_dict = {"active": active_player_sid, "disable": disable_player_sid}
    details.append(status_dict)
    emit('playgame active disable', details)


response = {}
@socketio.on('store response')
def store_response(details):
    player1_name = details[2]["player1"]
    player2_name = details[2]["player2"]
    active = details[1][player1_name]
    disable = details[1][player2_name]
    print("active: ", active)
    print("disable: ", disable)
    print("request_sid: ", request.sid)
    if request.sid == active:
        if active not in response:
            response[active] = [details[-1]["cellnumber"]]
        else:
            response[active].append(details[-1]["cellnumber"])
            if len(response[active]) >= 3:
                answer = check_for_winner(response[active])
        print("==entered==")
    emit('display msg', [active, disable])


def check_for_winner(active_list):
    pass


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug = True)

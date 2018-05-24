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
    if room not in players_connected:
        join_room(room)
        print("**first player added**")
        players_connected[room] = {request.sid: username}
        print("=============Room Info: ", players_connected)
        emit('user update', username + ' has joined the room.', room=room)
    elif len(players_connected[room]) == 1:
        join_room(room)
        print("**second player added**")
        players_connected[room].update({request.sid: username})
        print("=============Room Info: ", players_connected)
        emit('users joined', [username + ' has joined the room.', room, players_connected[room]], room=room)
    elif len(players_connected[room]) >= 2:
        emit('connection not established','There are already two people joined, you are not allowed to connect', room=request.sid)



@socketio.on('play game')
def play_game(details):
    active_player = next(myIterator)
    print("*****************************************", active_player)
    disable_player = 3 - active_player
    active_player_sid = details[2]["player" + str(active_player)][1]
    disable_player_sid = details[2]["player" + str(disable_player)][1]
    status_dict = {"active": [active_player_sid, active_player],
                   "disable": [disable_player_sid, disable_player]}
    details.append(status_dict)
    emit('playgame active', details, room=active_player_sid)
    emit('playgame disable', details, room=disable_player_sid)


response = {}
@socketio.on('store response')
def store_response(details):
    print("store response details: ", details)
    message = "Player{0} has marked at position {1}".format(details[0][3]["active"][1], details[1]["cellnumber"])
    emit('move msg', message, room=details[0][0])
    active = details[0][3]["active"][0]
    disable = details[0][3]["disable"][0]
    print("active: ", active)
    print("disable: ", disable)
    print("request_sid: ", request.sid)
    if request.sid == active:
        if active not in response:
            response[active] = [details[1]["cellnumber"]]
        else:
            response[active].append(details[1]["cellnumber"])
            if len(response[active]) >= 3:
                answer = check_for_winner(response[active])
                emit('display msg', [details, answer])
    else:
        emit('wrong turn', 'Not your turn', room=request.sid)


def check_for_winner(active_list):
    return "false"


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug = True)

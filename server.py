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
        player1 = [room, list(players_connected[room].keys()).pop(), list(players_connected[room].values()).pop()]
        players_connected[room].update({request.sid: username})
        print("=============Room Info: ", players_connected)
        emit('users joined', [username + ' has joined the room.', room, players_connected[room]], room=room)
        player2 = [room, request.sid, username]
        players = {"player1": player1, "player2": player2}
        details_to_send = [room, players_connected[room], players]
        print("***************************")
        print("details", details_to_send)
        print("***************************")
        play_game(details_to_send)

    elif len(players_connected[room]) >= 2:
        emit('connection not established','There are already two people joined, you are not allowed to connect', room=request.sid)


@socketio.on('play game again')
def play_game_again(details):
    play_game(details)


def play_game(details):
    print("EEEEENNNNNTTTTTTTEEEERRRRRRREEEEEEDDDDDDDDDDDDDDDDDDDDDDDD")
    print(details)
    print("***********************")
    active_player = next(myIterator)
    print("*****************************************", active_player)
    disable_player = 3 - active_player
    active_player_sid = details[2]["player" + str(active_player)][1]
    disable_player_sid = details[2]["player" + str(disable_player)][1]
    status_dict = {"active": [active_player_sid, active_player],
                   "disable": [disable_player_sid, disable_player]}
    details.append(status_dict)
    print("***************************")
    print("status", status_dict)
    print("***************************")
    emit('playgame active', details, room=active_player_sid)
    emit('playgame disable', details, room=disable_player_sid)


response = {}
@socketio.on('store response')
def store_response(details):
    print("====", request.sid, "====================store response details: ", details)
    room = details[0][0]
    message = "Player{0} has marked at position {1}".format(details[0][3]["active"][1], details[1]["cellnumber"])
    emit('move msg', message, room=details[0][0])
    active = details[0][3]["active"][0]
    disable = details[0][3]["disable"][0]
    print("active: ", active)
    print("disable: ", disable)
    print("request_sid: ", request.sid)
    if room not in response:
        response[room] = {}
    if request.sid == active:
        valid_var, validity_message = validity_check(response[room], details[1]["cellnumber"])
        if valid_var == "false":
            emit('playgame active', details[0], room=active)
            emit('playgame disable', details[0], room=disable)
        elif valid_var == "true":
            if active not in response[room]:
                print()
                print("====", request.sid, "#####################11111aaaa", response)
                response[room].update({active: [details[1]["cellnumber"]]})
                print("====", request.sid, "#####################11111bbbb", response)
                print()
                emit('display msg', [details, "false", "not enough number of moves"])
            else:
                print()
                print("====", request.sid, "#####################22222aaaaa", response)
                response[room][active].append(details[1]["cellnumber"])
                print("====", request.sid, "#####################22222bbbbb", response)
                print()
                if len(response[room][active]) >= 3:
                    player_name = details[0][1][active]
                    answer, message = check_for_winner(response[room][active], player_name)
                    emit('display msg', [details, answer, message], room=active)
    else:
        emit('wrong turn', 'Not your turn', room=request.sid)


def validity_check(response_dict, input):
    print("YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
    if input == "":
        return ["false", "some input between 1-9 is required"]
    try:
        int_input = int(input)
    except:
        return ["false", "input should be an integer between 1-9"]
    if int_input < 1 and int_input > 9:
        return ["false", "input should be an integer between 1-9"]
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", list(response_dict.values()))
    res_list = list(response_dict.values())
    total_res = []
    for one_list in res_list:
        total_res += one_list
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", total_res)
    print("^^^^^^^^^^^^^^^^^^^^^^^^6", int_input, "^^^^^^^^^^^^6", total_res)
    if str(int_input) in total_res:
        print("&&&&&&&&&&&&&&&&", int_input, "&&&&&&&&&&&&&&&&&", total_res)
        return ["false", "this cell is already taken"]
    return ["true", "data is valid"]


def check_for_winner(active_list, player_name):
    winner_list = [[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9],
                   [1, 4, 7],
                   [2, 5, 8],
                   [3, 6, 9],
                   [1, 5, 9],
                   [3, 5, 7]]
    for list in winner_list:
        if list[0] in active_list and list[1] in active_list and list[2] in active_list:
            return ["true", player_name + " wins"]
    return ["false", "No winner"]



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug = True)

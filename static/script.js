var socket = new io.connect('http://localhost:5000');

socket.on('connect', function() {
    console.log('connection established')
})


var button = document.getElementById('formButton')
console.log(button.id)
button.addEventListener('click', function(){
    console.log('inside on')
    var form = document.getElementById('submitForm');
    form.addEventListener('submit', function(e) {e.preventDefault()}, false)
    json_data = toJSONString(form)
    console.log(json_data);
    socket.emit('join player', json_data)
}, false)


socket.on('user update', function(msg) {
    console.log(msg)
    document.getElementById('player-joined').innerHTML = msg
})


socket.on('users joined', function(client_details) {
    console.log(client_details[0])
    console.log(client_details[1])
    console.log(client_details[2])
    msg = decidePlayers(client_details[1], client_details[2])
    document.getElementById('player-joined').innerHTML = client_details[0]
    var x = document.getElementById("playgame")
    x.style.display = "block"
    document.getElementById('player-role').innerHTML = msg[0]
    details = client_details.slice(1)
    details.push(msg[1])
    console.log("just before")
    console.log(details);
    socket.emit('play game', details)
})


socket.on('connection not established', function(conn_err_msg) {
    document.getElementById('player-joined').innerHTML = conn_err_msg
})


socket.on('playgame active', function(details) {
    console.log('inside playgame');
    document.getElementById('input').disabled = false
    document.getElementById('selectionButton').disabled = false
    var button = document.getElementById('selectionButton')
    console.log(button.id)
    button.addEventListener('click', function(){
        var form = document.getElementById('playgame');
        form.addEventListener('submit', function(e) {e.preventDefault()}, false)
        json_data = JSON.parse(toJSONString(form))
        console.log(json_data)
        console.log(details)
        socket.emit('store response', [details, json_data])
    }, false)
})


socket.on('playgame disable', function(details) {
    document.getElementById('input').disabled = true
    document.getElementById('selectionButton').disabled = true
})


socket.on('move msg', function(message) {
    document.getElementById('player-chance').innerHTML = message
})


socket.on('wrong turn', function(message) {
    document.getElementById('win-lose-draw').innerHTML = message
})


socket.on('display msg', function(details) {
    if(details[1] === "false"){
        new_details = details.slice(0, 3)
        socket.emit('play game', new_details)
    }
})


// function chanceMarkup(info) {
//     var chanceMarkup = `<p class = "player-chance">Player ${info[0]} placed mark on cell number ${info[1]}.</p>`
//     return chanceMarkup
// }
//


function decidePlayers(room, clientsInRoom){
    clientList = Object.keys(clientsInRoom)
    player1 = clientList[0]
    player2 = clientList[1]
    player_details = {"player1": [room, player1, clientsInRoom[player1]],
                      "player2": [room, player2, clientsInRoom[player2]]}
    display_msg = 'Player1 is ' + clientsInRoom[player1] + ' and Player2 is ' + clientsInRoom[player2]
    return [display_msg, player_details]
}


function toJSONString(form) {
    var obj = {};
    var elements = form.querySelectorAll('input');
    for (var i = 0; i < elements.length; ++i) {
        var element = elements[i];
        var name = element.name;
        var value = element.value;
        if (name) {
            obj[name] = value;
        }
    }
    return JSON.stringify(obj);
}

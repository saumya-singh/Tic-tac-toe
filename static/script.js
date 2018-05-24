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
    msg = decidePlayers(client_details[2])
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


function chanceMarkup(info) {
    var chanceMarkup = `<p class = "player-chance">Player ${info[0]} placed mark on cell number ${info[1]}.</p>`
    return chanceMarkup
}


socket.on('playgame active disable', function(details) {
    console.log('inside playgame');
    var button = document.getElementById('selectionButton')
    console.log(button.id)
    button.addEventListener('click', function(){
        var form = document.getElementById('playgame');
        form.addEventListener('submit', function(e) {e.preventDefault()}, false)
        json_data = toJSONString(form)
        details.push(JSON.parse(json_data))
        console.log(json_data) ////////////////
        console.log(details)
        chanceMarkup()
        socket.emit('store response', details)
    }, false)
})


function decidePlayers(clientsInRoom){
    clientList = Object.keys(clientsInRoom)
    player1 = clientList[0]
    player2 = clientList[1]
    player_details = {"player1": player1, "player2": player2}
    display_msg = 'Player1 is ' + player1 + ' and Player2 is ' + player2
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

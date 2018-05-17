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
    // window.location="http://www.tutorialspoint.com"
})


socket.on('users joined', function(client_details) {
    console.log(client_details[0])
    console.log(client_details[1])
    console.log(client_details[2])
    // window.alert(client_details[0])
    document.getElementById('player-joined').innerHTML = client_details[0]
    var x = document.getElementById("playgame");
    x.style.display = "block";
    socket.emit('select player', client_details.slice(1))
})


socket.on('display', function(player_details) {
    display_msg = 'Player1 is ' + player_details[0]["player1"] + ' and Player2 is ' + player_details[0]["player2"]
    window.alert(display_msg)
    // player_details[0]
    // player_details[1]
    // player_details[2]
})


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

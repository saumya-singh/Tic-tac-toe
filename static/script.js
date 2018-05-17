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
    socket.emit('join_player', json_data)
}, false)


socket.on('user update', function(msg) {
    console.log(msg)
    window.alert(msg)
    // window.location="http://www.tutorialspoint.com"
})


socket.on('users joined', function(msg) {
    console.log(msg[0])
    console.log(msg[1])
    console.log(msg[2])
    window.alert(msg[0])
    var x = document.getElementById("playgame");
    x.style.display = "block";
    socket.emit('select player', msg[1:])
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

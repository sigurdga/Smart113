var socket = io.connect('http://localhost:1337');
socket.on('call', function (data) {
    console.log(data);
    var time = new Date();
    if (data.match) {
        var bgclass = " match";
    } else {
        var bgclass = "";
    }
    $('#calls').prepend('<div class="well' + bgclass + '"><h2><a href="/c/search/' + jQuery.trim(data.number) + '">' + jQuery.trim(data.number) +'</a></h2>' + data.results.map(function(item) { return '<p><a href="p/' + item.id + '">' + item.name + ' (' + item.city + ')</a><br>' + time.getHours() + ":" + time.getMinutes() + '</p>' }).join(", "));
    //socket.emit('ret', { data: data }); // maybe later
});

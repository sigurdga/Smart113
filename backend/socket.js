var io = require('socket.io').listen(1337);

io.sockets.on('connection', function (socket) {
  socket.emit('news', { hello: 'world' });
});

var net = require('net');
var server = net.createServer(function(c) { //'connection' listener
  console.log('server connected');
  c.on('end', function() {
    console.log('server disconnected');
  });
  c.on('data', function(obj) {
    console.log("received: " +obj.toString());
    io.sockets.emit('call', JSON.parse(obj));
  });
});
server.listen('7777', function() { //'listening' listener
  console.log('server bound');
});

/*
process.stdin.resume();
process.stdin.setEncoding('utf8');

process.stdin.on('data', function (chunk) {
  process.stdout.write('data: ' + chunk);
  io.sockets.emit('phone', { number: chunk });
});

process.stdin.on('end', function () {
  process.stdout.write('end');
});
*/

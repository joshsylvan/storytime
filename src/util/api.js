import io from 'socket.io-client';

export const connectToServer = (connect, event, disconnect) => {

  const socket = new io('http://192.168.0.11:5000');

  socket.on('connect', function () {
    // console.log('connected');
    // socket.emit('hello', {
    //   clone: 'hello'
    // });
  });
  // socket.on('event', function (data) {
  // });
  event(socket);
  socket.on('disconnect', function () { console.log('NOPE') });

  return socket;
};
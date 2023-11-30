import socketio

sio = socketio.Client()


@sio.event
def connect():
    print("I'm connected!")


@sio.event
def disconnect():
    print("I'm disconnected!")


sio.connect('http://localhost:5000')

while True:
    input("Waiting for button press")
    sio.emit('change_slide', {'action': 'next'})

from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import randint

app = Flask(__name__)
io = SocketIO(app)

clients = []

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/viewer')
def display_viewer():
    return render_template('viewer.html')

@app.route('/controller')
def display_controller():
    return render_template('controller.html');

@io.on('connect')
def connected():
    print("Someone has connected")
    #print("%s connected" % (request.namespace.socket.sessid))
    #clients.append(request.namespace)

@io.on('requestId')
def sendId():
    id = randint(0,10000);
    print("Sending id: " + str(id));
    io.emit('id', id);

@io.on('disconnect')
def disconnect():
    print("Someone has disconnected")
    #print("%s disconnected" % (request.namespace.socket.sessid))
    #clients.remove(request.namespace)


if __name__ == '__main__':
    io.run(app)
#if __name__ == '__main__':
#    app.run()

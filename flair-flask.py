from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO
from random import randint
from flask.ext.mobility import Mobility
import os

app = Flask(__name__)
Mobility(app)
io = SocketIO(app)

controllers = []
displays = []

@app.route('/')
def hello_world():
    if request.MOBILE:
        return redirect("/controller", code=302)

    return redirect("/viewer", code=302)


@app.route('/viewer')
def display_viewer():
    return render_template('viewer.html')


@app.route('/controller')
def display_controller():
    return render_template('controller.html');


@io.on('connect')
def connected():
    print("%s connected" % (request.sid))



@io.on('requestIdController')
def sendId():
    id = randint(0,10000);
    print("Sending id: " + str(id));
    controllers.append((request.sid, id));
    io.emit('id', id);

@io.on('initDisplay')
def sendId(id):

    for tuple in controllers:
        if(id == tuple[1]):
            displays.append((request.sid, id))
            print("Initializing display with id" + str(id))
            io.emit('success')
            io.emit('startController', id, room=tuple[0]);
            return

    print("Controller not found :(")
    io.emit('notfound')

@io.on('data')
def sendData(data):

    id=-1;

    for tuple in controllers:
        if(request.sid == tuple[0]):
            id=tuple[1]
            break

    if(id != -1):
        for tuple in displays:
            if(id == tuple[1]):
                io.emit('data',data,room=tuple[0]);
                break

@io.on('disconnect')
def disconnect():
    print("%s disconnected" % (request.sid))

    for tuple in controllers:
        if(request.sid == tuple[0]):
            controllers.remove(tuple)
            break

    for tuple in displays:
        if(request.sid == tuple[0]):
            for tuple2 in controllers:
                if(tuple[1]==tuple2[1]):
                    io.emit('stopController', room=tuple2[0])
                    break
            controllers.remove(tuple)
            break



if __name__ == '__main__':
    port=int(os.environ.get("PORT", 5000))
    io.run(app,host= '0.0.0.0', port=port)

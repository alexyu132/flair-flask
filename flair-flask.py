from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO
from random import randint
from flask.ext.mobility import Mobility

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
    exists=False

    for tuple in controllers:
        if(id == tuple[1]):
            exists=True

    if(exists):
        displays.append((request.sid, id))
        print("Initializing display with id" + str(id))

@io.on('disconnect')
def disconnect():
    print("%s disconnected" % (request.sid))

    for tuple in controllers:
        if(request.sid == tuple[0]):
            controllers.remove(tuple)

    for tuple in displays:
        if(request.sid == tuple[0]):
            controllers.remove(tuple)



if __name__ == '__main__':
    io.run(app,host= '0.0.0.0')

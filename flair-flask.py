from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO
from flask.ext.mobility import Mobility
app = Flask(__name__)
Mobility(app)
io = SocketIO(app)

clients = []

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
    print("Someone has connected")
    #print("%s connected" % (request.namespace.socket.sessid))
    #clients.append(request.namespace)


@io.on('disconnect')
def disconnect():
    print("Someone has disconnected")
    #print("%s disconnected" % (request.namespace.socket.sessid))
    #clients.remove(request.namespace)


if __name__ == '__main__':
    io.run(app)
#if __name__ == '__main__':
#    app.run()

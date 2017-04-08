from flask import Flask
from flask_socketio import SocketIO,
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@socketio.on('datapoint')
def data_point_response(message)
   emit('datapoint', {'x':message.x,'y':message.y,'z':message.z})

if __name__ == '__main__':
    app.run()

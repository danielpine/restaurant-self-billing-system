from flask import (Flask, Response, escape, jsonify, redirect, request, session, url_for)
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer
from flask_sockets import Sockets
from ShapeDetector import detect
import time

app = Flask(__name__, static_url_path='')
sockets = Sockets(app)
app.config['DEBUG'] = True
user_socket_list = []

@app.route('/')
def index():
    return app.send_static_file('index.html')

@sockets.route('/socket')
def socket(ws):
    while not ws.closed:
        try:
            msg = ws.receive()
            print(len(msg))
            start=time.time()
            result = detect(msg)
            print("time:"+str(time.time()-start))
            ws.send(result)
        except Exception as e:
            e.__traceback__()

if __name__ == "__main__":
    srv = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    print(u'Starting WSGIServer...')
    srv.serve_forever()

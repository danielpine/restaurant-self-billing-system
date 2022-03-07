from flask import (Flask, Response, escape, jsonify, redirect, request,
                   session, url_for)
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer

from ShapeDetector import detect

app = Flask(__name__, static_url_path='')
app.config['DEBUG'] = True
user_socket_list = []
import time

@app.route('/socket')
def socket():
    user_socket = request.environ.get('wsgi.websocket')
    print('request %s', request)
    print('user_socket %s', user_socket)
    if user_socket:
        user_socket_list.append(user_socket)
        print('user_socket_list depth %s', len(user_socket_list))
    while True:
        try:
            msg = user_socket.receive()
            print(len(msg))
            start=time.time()
            result = detect(msg)
            print("time:"+str(time.time()-start))
            user_socket.send(result)
        except Exception as e:
            e.__traceback__()
            if user_socket and user_socket in user_socket_list:
                user_socket_list.remove(user_socket)
            return ''


if __name__ == "__main__":
    srv = WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
    print(u'Starting WSGIServer...')
    srv.serve_forever()

import json
import logging
import sys
import traceback

import tornado
import tornado.websocket
from tools.ShapeDetector import detect

from controller import route

sys.path.append("..")
sys.path.append(".")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


@route(r'/socket')
class WebsocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        '''重写同源检查 解决跨域问题'''
        return True

    def open(self):
        '''新的websocket连接后被调动'''
        # self.write_message('Welcome')
        print('connected...')

    def on_close(self):
        '''websocket连接关闭后被调用'''
        print('closed...')

    def on_message(self, message):
        '''接收到客户端消息时被调用'''
        try:
            message = json.loads(message)
            result = detect(message)
            self.write_message(result)  # 向客服端发送
        except Exception as e:
            traceback.print_exc()


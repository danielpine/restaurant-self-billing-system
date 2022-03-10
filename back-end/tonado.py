from pickletools import uint4
from posixpath import split
import uuid
import json
import logging
import tornado.ioloop
import tornado.web
import tornado.websocket
from ShapeDetector import detect
import traceback

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


class ConnectHandler(tornado.websocket.WebSocketHandler):
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


users = {}


def generateAccessToken():
    return ''.join(str(uuid.uuid4()).split('-'))


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.warn(form)
        token = generateAccessToken()
        self.write({"code": 200, "msg": "success",
                   "data": {"accessToken": token}})
        if 'visitor' in form:
            users[token] = {"roles": ["visitor"],
                            "ability": ["READ", "WRITE", "DELETE"],
                            "username": "visitor",
                            "avatar": "https://i.gtimg.cn/club/item/face/img/8/15918_100.gif"
                            }
        else:
            users[token] = {"roles": ["admin"],
                            "ability": ["READ", "WRITE", "DELETE"],
                            "username": "admin",
                            "avatar": "https://i.gtimg.cn/club/item/face/img/8/15918_100.gif"
                            }


class UserInfoHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.warn(form)
        token = form['accessToken']
        if token in users:
            self.write({"code": 200,
                        "msg": "success",
                        "data": users[token]})
        else:
            self.write({"code": 400,
                        "msg": "Token timed out,please login!"})


class LogoutHandler(tornado.web.RequestHandler):
    def post(self):
        self.write({"code": 200, "msg": "success"})


if __name__ == "__main__":
    app = tornado.web.Application(
        [
            (r'/socket', ConnectHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler),
            (r'/userInfo', UserInfoHandler),
        ]
    )
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()

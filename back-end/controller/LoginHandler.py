import json

import tornado
import logging
import sys

from tools.PySqlTemplate import PySqlTemplate
from controller import route
from service import LoginService
from tools import generateAccessToken
sys.path.append("..")
sys.path.append(".")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
users = {}
loginService = LoginService()


def getUserInfoByToken(token):
    if token in users:
        return users[token]
    else:
        return None


@route(r'/logout')
class LogoutHandler(tornado.web.RequestHandler):
    def post(self):
        self.write({"code": 200, "msg": "success"})


@route(r'/login')
class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.warn(form)
        token = generateAccessToken()
        # 游客登录
        if 'visitor' in form:
            users[token] = {"roles": ["visitor"],
                            "ability": ["READ", "WRITE", "DELETE"],
                            "username": "visitor",
                            'user_id': 0,
                            "avatar": "https://i.gtimg.cn/club/item/face/img/8/15918_100.gif"}
            self.write({"code": 200, "msg": "success",
                        "data": {"accessToken": token}})
            return
        # 校验用户
        user = loginService.findUser(form['username'], form['password'])
        if user:
            self.write({"code": 200, "msg": "success",
                       "data": {"accessToken": token}})
            users[token] = {"roles": [user['role']],
                            "ability": ["READ", "WRITE", "DELETE"],
                            "username": user['username'],
                            'user_id': user['user_id'],
                            "avatar": "https://i.gtimg.cn/club/item/face/img/8/15918_100.gif"}
        else:
            self.write({"code": 400,
                        "msg": "username or password is incorrect!"})


@route(r'/userInfo')
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

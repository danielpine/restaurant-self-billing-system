import json
import logging
import sys
import time

import tornado
from tools.PySqlTemplate import PySqlTemplate

from controller import route
from controller.LoginHandler import getUserInfoByToken

sys.path.append("..")
sys.path.append(".")
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


@route(r'/hasUser')
class HasUserHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.info(form)
        count = PySqlTemplate.count(
            'select count(*) from user where username=?', form['username'])
        self.write({"code": 200, "msg": "success", "data": count})


@route('/register')
class RegisterHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.info(form)
        if 'user' in form and 'pass' in form:
            PySqlTemplate.save(
                'INSERT INTO user(username, passwd, role) VALUES (?,?,?)', form['user'], form['pass'], 'member')
            self.write({"code": 200, "msg": "success", "data": 'ok'})
        else:
            self.write(
                {"code": 400, "msg": "invalid parameters", "data": 'no'})

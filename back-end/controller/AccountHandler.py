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


@route(r'/charge')
class AccountHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.info(form)
        token = form['accessToken']
        user = getUserInfoByToken(token)
        log.info(user)
        if user:
            balance = form['detail']['amount']
            balancePo = PySqlTemplate.findOne(
                'select * from balance where user_id=?', user['user_id'])
            if not balancePo:
                PySqlTemplate.save(
                    'INSERT INTO balance(user_id, balance) VALUES (?,?)', user['user_id'], balance)
            else:
                balance = balance + balancePo['balance']
                PySqlTemplate.save(
                    'update balance set balance=? where user_id=?', balance, user['user_id'])

            self.write({"code": 200, "msg": "success", "data": balance})
        else:
            self.write({"code": 400,
                        "msg": "Token timed out,please login!"})


@route(r'/discount')
class DiscountHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.info(form)
        token = form['accessToken']
        user = getUserInfoByToken(token)
        log.info(user)
        if user:
            count = PySqlTemplate.count(
                'select count(*) from orders where user_id=? and month=?', user['user_id'], time.strftime("%Y%m", time.localtime()))
            self.write({"code": 200, "msg": "success", "data": count})
        else:
            self.write({"code": 400, "msg": "Token timed out,please login!"})


@route(r'/balance')
class BalanceHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.info(form)
        token = form['accessToken']
        user = getUserInfoByToken(token)
        log.info(user)
        if user:
            balancePo = PySqlTemplate.findOne(
                'select * from balance where user_id=?', user['user_id'])
            if not balancePo:
                self.write({"code": 200, "msg": "success", "data": 0})
            else:
                self.write({"code": 200, "msg": "success",
                           "data": balancePo['balance']})

        else:
            self.write({"code": 400, "msg": "Token timed out,please login!"})


@route(r'/pay')
class PayHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.info(form)
        token = form['accessToken']
        user = getUserInfoByToken(token)
        log.info(user)
        if user:
            if form['mode'] == 'balance':
                balancePo = PySqlTemplate.findOne(
                    'select * from balance where user_id=?', user['user_id'])
                if not balancePo or balancePo['balance'] < form['order']['pay']:
                    self.write({
                        "code": 400,
                        "msg": "the balance is insufficient, please recharge it first"
                    })
                else:
                    PySqlTemplate.save(
                        'update balance set balance=? where user_id=?',
                        balancePo['balance'] - form['order']['pay'],
                        user['user_id'])
                    PySqlTemplate.save(
                        'INSERT INTO orders(user_id, user_name, sum, order_type, items, month) VALUES (?,?,?,?,?,?)',
                        user['user_id'],
                        user['username'],
                        form['order']['pay'],
                        form['mode'],
                        json.dumps(form['order'], ensure_ascii=False),
                        time.strftime("%Y%m", time.localtime())
                    )
                    self.write({"code": 200, "msg": "支付成功",  "data": "支付成功", })
            else:
                PySqlTemplate.save(
                    'INSERT INTO orders(user_id, user_name, sum, order_type, items, month) VALUES (?,?,?,?,?,?)',
                    user['user_id'],
                    user['username'],
                    form['order']['pay'],
                    form['mode'],
                    json.dumps(form['order'], ensure_ascii=False),
                    time.strftime("%Y%m", time.localtime()))
                self.write({"code": 200, "msg": "支付成功",  "data": "支付成功", })
        else:
            self.write({"code": 400,  "msg": "Token timed out,please login!"})

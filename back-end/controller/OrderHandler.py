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


@route(r'/table/getList')
class OrderListHandler(tornado.web.RequestHandler):
    def get(self):
        pageSize = self.get_query_argument('pageSize')
        log.info(pageSize)
        current = self.get_query_argument('current')
        log.info(current)
        total = PySqlTemplate.count('select count(*) from orders')
        page = PySqlTemplate.findList(
            'select * from orders limit ?,?', (int(current)-1)*int(pageSize), int(pageSize))
        self.write({
            'code': 200,
            'msg': 'success',
            'total': total,
            'columns': [
                {
                    'title': '#',
                    'dataIndex': 'id',
                },
                {
                    'title': 'UserId',
                    'dataIndex': 'user_id',
                },
                {
                    'title': 'UserName',
                    'dataIndex': 'user_name',
                },
                {
                    'title': 'Amount(CNY)',
                    'dataIndex': 'sum',
                },
                {
                    'title': 'OrderType',
                    'dataIndex': 'order_type',
                },
                {
                    'title': 'Month',
                    'dataIndex': 'month',
                },
                {
                    'title': 'Time',
                    'dataIndex': 'create_time',
                },
            ],
            'data': page,
        })


@route(r'/table/getUsers')
class UserListHandler(tornado.web.RequestHandler):
    def get(self):
        pageSize = self.get_query_argument('pageSize')
        log.info(pageSize)
        current = self.get_query_argument('current')
        log.info(current)
        total = PySqlTemplate.count('select count(*) from user')
        page = PySqlTemplate.findList(
            'select * from user where username<>? limit ?,?', 'admin', (int(current)-1)*int(pageSize), int(pageSize))
        self.write({
            'code': 200,
            'msg': 'success',
            'total': total,
            'columns': [
                {
                    'title': 'UserId',
                    'dataIndex': 'user_id',
                },
                {
                    'title': 'UserName',
                    'dataIndex': 'username',
                },
                {
                    'title': 'Role',
                    'dataIndex': 'role',
                },
            ],
            'data': page,
        })


@route(r'/table/getItems')
class ItemsHandler(tornado.web.RequestHandler):
    def get(self):
        pageSize = self.get_query_argument('pageSize')
        log.info(pageSize)
        current = self.get_query_argument('current')
        log.info(current)
        total = PySqlTemplate.count('select count(*) from items')
        page = PySqlTemplate.findList(
            'select * from items limit ?,?', (int(current)-1)*int(pageSize), int(pageSize))
        self.write({
            'code': 200,
            'msg': 'success',
            'total': total,
            'data': page,
        })


@route(r'/item/save')
class ItemSaveHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.info(form)
        key = None
        if 'id' in form:
            key = form['id']
            PySqlTemplate.delete('delete from items where id=?', key)
        else:
            key = PySqlTemplate.count('select IFNULL(max(id),0) from items')+1
        PySqlTemplate.save(
            'INSERT INTO items(id,item_name, item_type, item_price) VALUES (?,?,?,?)', key, form['item_name'], form['item_type'], form['item_price'])
        self.write(
            {"code": 200, "msg": "done", "data": key})

@route(r'/item/updateInventory')
class ItemSaveHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.info(form)
        key = None
        if 'id' in form:
            key = form['id']
            PySqlTemplate.save('update items set inventory=? where id=?',form['inventory'],key)
            self.write({"code": 200, "msg": "done", "data": key})
        else:
            self.write(
                {"code": 400, "msg": "id not found"})


@route(r'/item/del')
class ItemDelHandler(tornado.web.RequestHandler):
    def post(self):
        form = json.loads(self.request.body)
        log.info(form)
        key = None
        if 'id' in form:
            key = form['id']
            PySqlTemplate.delete('delete from items where id=?', key)
            self.write(
                {"code": 200, "msg": "done", "data": key})
        else:
            self.write(
                {"code": 400, "msg": "id not found"})

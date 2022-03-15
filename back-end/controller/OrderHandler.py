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

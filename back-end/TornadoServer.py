import logging

import tornado.ioloop
import tornado.web

from controller import routes
from tools import routeScan, setupDataSource
from tools.common import getPythonDataBase

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

routeScan('controller')
setupDataSource(getPythonDataBase())


if __name__ == "__main__":
    app = tornado.web.Application(routes, debug=True)
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()

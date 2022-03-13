import logging
import sys

from tools.PySqlTemplate import PySqlTemplate
sys.path.append("..")
sys.path.append(".")

fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=fmt)
log = logging.getLogger(__name__)


class LoginService(object):

    def findUser(self, user, passwd):
        return PySqlTemplate.findOne('select * from user where username=? and passwd=?', user, passwd)

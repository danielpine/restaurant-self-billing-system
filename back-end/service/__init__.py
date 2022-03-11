import logging
import sys
sys.path.append("..")

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

class LoginService(object):
    def __init__(self) -> None:
        pass

    def findUser(self, user, passwd):
        log.info(user, passwd)
        pass

import time
import logging

logger = logging.getLogger(__name__)

class othermodule (object):

    def  __init__(self):
        # self.log = logging.getLogger('main.othermodule.othermodule')
        self.log = logger
        self.test = None
        # self.log = True

    def  run(self):
        logger = logging.getLogger(__name__)
        logger.info("Hello, this is printed from othermodule class by loggerget")
        self.log.info("Hello, this is printed from othermodule class")
        time.sleep(1)
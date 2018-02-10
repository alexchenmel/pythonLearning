# /bash/python

import time
import logging
import othermodule

logger = logging.getLogger(__name__)

# class othermodule (object):
#
#     def  __init__ (self):
#         self.log = logging.getLogger('othermodule')
#         self.test = None
#
#
#     def  run(self):
#         if self.log:
#             self.log.info("Hello, this is printed from othermodule class")
#         else:
#             print('Logger is not exist in othermodule')
#         time.sleep(1)

class baselog (object):

    def  __init__ (self):
        self.log = logging.getLogger(self.__class__.__name__)
        # self.log = logger
        # self.log = logger.getChild('baselog')
        self.test = None
        self.others = othermodule.othermodule()


    def  run(self):
        if self.log:
            self.log.info("Hello, this is printed from baselog class")
        time.sleep(1)
        self.others.run()


class layer1log (baselog):
    def __init__(self):
        super(layer1log, self).__init__()
        self.log = logging.getLogger(self.__class__.__name__)
        # self.log = logger.getChild('layerlog')
        # self.log = logger
        # self.log.setLevel(logging.DEBUG)
        # fh = logging.FileHandler('testlog.log')
        # fh.setLevel(logging.DEBUG)
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # ch.setFormatter(formatter)
        # fh.setFormatter(formatter)
        # self.log.addHandler(ch)
        # self.log.addHandler(fh)


    def runTop (self):
        if self.log:
            self.log.info("Hello, this is from lay1log")


if __name__ == "__main__":
    # logger = logging.getLogger('root')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('testlog.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    testlog = layer1log()
    testlog.run()
    testlog.runTop()
    otherm = othermodule.othermodule()
    otherm.run()




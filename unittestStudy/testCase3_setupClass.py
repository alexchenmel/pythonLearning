#!/bin/sh
#
#
#

import time
import logging
import unittest

from uutclass import UutClass

def setUpModule():
    global logger
    logger = logging.getLogger(__name__)
    logging.basicConfig()
    logger.debug("start running module test {}".format(__name__))

class testAddDelMethod(unittest.TestCase):

    # def __init__(self):
    #
    #     super(testAddDelMethod,self).__init__()
    #     self.uutInst = UutClass()
    @classmethod
    def setUpClass(self):                # will run every time before call each test method, here will call twice
        logger.info('Running from setup class')
        # unittest.installHandler()
        self.uutInst = UutClass()

    def testAdd(self):
        uutCount = self.uutInst.count
        self.uutInst.addThings('OK')
        self.assertEqual(self.uutInst.count, uutCount+1)

    def testDel(self):
        self.uutInst.addThings('OK')
        uutCount = self.uutInst.count
        self.uutInst.delThings()
        self.assertEqual(self.uutInst.count, uutCount-1)

if __name__ == '__main__':
    unittest.main()
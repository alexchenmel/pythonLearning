#!/bin/sh
#
#
#

import time
import logging
import unittest

from uutclass import UutClass
# uutInst = UutClass()

class testAddDelMethod(unittest.TestCase):


    def testAdd(self):
        uutInst = UutClass()
        uutInst.addThings('OK')
        self.assertEqual(uutInst.count, 1)

    def testDel(self):
        uutInst = UutClass()
        uutInst.addThings('OK')
        uutInst.addThings('Done')
        uutInst.delThings()
        self.assertEqual(uutInst.count, 1)


if __name__ == '__main__':
    unittest.main()
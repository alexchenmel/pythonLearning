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

    def setUp(self):                # will run every time before call each test method, here will call twice
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
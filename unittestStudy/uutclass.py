#!/bin/sh

import logging
import time

class UutClass(object):

    def __init__(self):
        self.result = None
        self.flag = False
        self.things = []
        self.count = 0

    def addThings(self, thing):

        if thing:
            self.things.append(thing)
            self.count = self.count+1

    def delThings(self):
        self.things.pop()
        self.count = self.count-1


if __name__ == '__main__':
    uutInst = UutClass()
    uutInst.addThings('hello')
    print (uutInst.count)
    uutInst.delThings()
    print(uutInst.count)
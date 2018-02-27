#
# help classes
#
# Includes:
#  Async Buffer interface

class AsyncBuffer(object):
    def __init__(self, size=8196):
        self._buf = [0*size]
        self._len = 0
        self._size = size

    @property
    def length(self):
        return self._len

    @property
    def empty(self):
        return True if self._len == 0 else False

    @property
    def full(self):
        return True if self._len == self._size else False

    def push(self, data):
        if self._len >= 8196:
            raise Exception('Buff is full')
        else:
            self._buf.append(data)
            self._len += 1

    def pop(self):
        if self._len == 0:
            raise Exception('Buff is empty')
        else:
            self._len -= 1
            return self._buf.pop()
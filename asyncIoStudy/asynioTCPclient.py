#!/bin/sh
#
#
#

import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('asyncio')

@asyncio.coroutine
def tcp_client(message, loop):
    reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888, loop = loop)
    loop = asyncio.get_event_loop()
    loop.create_task(recv(reader))
    loop.create_task(transmit(writer, message))

@asyncio.coroutine
def recv(steamReader):
    while True:
        data = yield from steamReader.read(100)
        log.debug('Received: {}'.format(data.decode()))
        # yield from asyncio.sleep(1)

@asyncio.coroutine
def transmit(streamWrite, data):
    while True:
        log.debug('Send: {}'.format(data))
        streamWrite.write(data)
        yield from streamWrite.drain()
        yield from asyncio.sleep(0.1)

loop = asyncio.get_event_loop()

for i in range(1):
    message = '<LOG?;SGN="abc{}";TT{}="CMD">'.format(i,i)
    loop.create_task(tcp_client(message.encode(),loop))
loop.run_forever()
loop.close()
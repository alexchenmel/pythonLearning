#!/bin/sh
#
#
#

import asyncio
from asyncio import AbstractEventLoop
import logging
import re

RMS_CMD_START = '<'
RMS_CMD_END = '>'
RMS_CMD_SEP = ';'

log = logging.getLogger('asyncio').setLevel(logging.WARNING)

taskLists = []
sessionLists = []
writeBuffer=[]

# command Parse better to move to process task instead of receiver task
def commandParse(message):
    ''' the command parser
        the command format is : < cmd1=xxx;cmd2=xxx;cmd3=xxx >
    '''
    result = [] # use list to make sure command sequence same as incoming message
    cmdArray = message[1:-1].split(RMS_CMD_SEP)  # remove start and end bracket '<' and '>'
    # result = [[cmd[0:3], 'query' if cmd[3] and cmd[3] == '?' else 'report', cmd[4:] if cmd[4] and cmd[3]=='='] for
    #           cmd in cmdArray ]
    for cmd in cmdArray:
        cmdListTemp= []
        cmdListTemp.append(cmd[0:3])
        if cmd[3]:
            if cmd[3]=='?':
                cmdListTemp.append('query')
            elif cmd[3] == '=':
                cmdListTemp.append('report')
                if cmd[4]:
                    cmdListTemp.append(cmd[4:])
                else:
                    cmdListTemp[1] = 'invalid'
            else:
                cmdListTemp.append('invalid')
        elif cmd[4]:
            cmdListTemp.append('invalid')
        else:
            cmdListTemp.append('special')
        result.append(cmdListTemp)

    return result

@asyncio.coroutine
def connectHandler(streamReader,streamWriter):
    global sessionLists
    #create session once there is connection requested
    sessionInfo = ['peername', 'sock', 'sockname']
    sessInst = {}
    for sessInfo in sessionInfo:
        sessInst[sessInfo] = streamWriter.get_extra_info(sessInfo)

    sessionLists.append(sessInst)

    eventLoop = asyncio.get_event_loop()  #which means you can't use AbstractEventLoop directly
    #create Receiver and Transmit task
    taskLists.append(eventLoop.create_task(tcpReceiver(streamReader)))
    taskLists.append(eventLoop.create_task(tcpTransmitter(streamWriter)))

    # #create Receiver and Transmit task
    # taskLists.append(AbstractEventLoop.create_task(tcpReceiver, streamReader))
    # taskLists.append(AbstractEventLoop.create_task(tcpTransmitter,streamWriter))

# task to receive message from socket, and if got message, check if valid message
# if it is, create and yield task to process it
async def tcpReceiver(streamReader):
    data = await streamReader.readuntil(RMS_CMD_END)
    message = data.decode()
    log.debug('Received:{}'.format(message))
    eventLoop = asyncio.get_event_loop()  # which means you can't use AbstractEventLoop directly
    taskProcess = eventLoop.create_task(process_message(message))
    # taskProcess = AbstractEventLoop.create_task(process_message, message)
    taskLists.append(taskProcess)

    # cmd = commandParse(message)
    # if cmd:
    #     taskProcess = AbstractEventLoop.create_task(process_message, message)
    #     taskLists.append(taskProcess)
    # else:
    #     log.warn('Invalid message received')
    #     pass

# task for process receiver message
async def process_message(message):
    cmdLists = commandParse(message)
    for cmd in cmdLists:
        if cmd[1] == 'query':
            log.info('Query CMD : {} received'.format(cmd[0]))
            #TODO: either use lock to share same writer buffer or some sort of message hub to pass the data
            # to the transmitter task
        elif cmd[1] == 'report':
            log.info('Report CMD: {} received; Report Message: {}'.format(cmd[0],cmd[2]))
            #TODO: put it into database or put into message bus to let other task process it
        elif cmd[1] == 'special':
            log.info('Special message: {} received'.format(cmd[0]))
            #TODO: process it by call other task
        else:   # invalid message
            pass


# task to send TCP data from server to destination if there are data available in write buffer
# (TODO:) two scenarios,
# 1. if there is no TCP connection exist, it require send UDP message to target to let target to create TCP connection
# request,
# 2. just send it because the writer is actually created after connection request accepted by server
# so either before sending it, to make sure TCP connection already create it or let other process to determine it
# accordingly
async def tcpTransmitter(streamWriter):
    while True:
        data = writeBuffer.pop()
        if data:
            streamWriter.write(data)
            await streamWriter.drain()
        else:
            log.warn('Something wrong with writer buffer')
            pass


async def pump_data_test():
    while True:
        i = i + 1
        data = 'Hello, world {}'.format(i)
        writeBuffer.append(data)
        asyncio.sleep(1)


loop = asyncio.get_event_loop()
coro = asyncio.start_server(connectHandler, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()

except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()


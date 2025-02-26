'''

Модуль драйвера для керування приводом

Выполняет следующие действия:
1. синхронна передача команд керування по порту RS232
2. Асинхронний прийом міток  i команд для бд по Zmq (json) :7002
3. збереження в бд influx.db  (json)


'''
import asyncio
import sys
import this
import tracemalloc
#import numpy
import zmq
import time
import random
import serial
#from drv_reader_async import Reader_Async
from drv_zmq_sub_vfd import Zmq_Sub


#async def rs232_reader():
def getSyncReader():

    '''
    baudrate=9600,
	bytesize=serial.EIGHTBITS,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_TWO,
	timeout=1,
	write_timeout=0,
	xonxoff=False,
	rtscts=False,
 	dsrdtr=False  

    port = '/dev/ttyUSB4'

    serial_port_vfd = serial.Serial(
    port=port,
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    timeout=1, 
    write_timeout=0,
    xonxoff=False,
    rtscts=False,
    dsrdtr=False)  
    
    '''
    #port = '/dev/ttyUSB4'
    port = '/dev/ttyMXUSB4'
    baudrate=9600
    bytesize=serial.EIGHTBITS
    parity=serial.PARITY_NONE
    stopbits=serial.STOPBITS_TWO
    timeout=1 
    write_timeout=0
    xonxoff=False
    rtscts=False
    dsrdtr=False

    #self.
    #reader_async = Reader_Async(port,baudrate,bytesize,parity,stopbits,write_timeout,xonxoff,rtscts,dsrdtr)
    reader_sync = serial.Serial(port,baudrate,bytesize,parity,stopbits,timeout,write_timeout,xonxoff,rtscts,dsrdtr)

    print("Doing rs232_reader")
    #reader_async.reader()
    return reader_sync


#async def zmq_sub():
def getZmqSub():

    #bind_to = "tcp://localhost:7002" 
    bind_to = "tcp://localhost:7001" 

    zmq_sub = Zmq_Sub(bind_to) 

    print("Doing the zmq_sub")
    #asyncio.run(zmq_sub.subscribe())
    #zmq_sub.subscribe()
    return zmq_sub


async def main():
        tracemalloc.start()
        zmq_sub = getZmqSub()
        rs232_reader = getSyncReader()       
        
        tasks = []
        tasks.append(asyncio.create_task(rs232_reader.reader()))
        tasks.append(asyncio.create_task(zmq_sub.subscribe()))
        
        await asyncio.gather(*tasks)
        

asyncio.run(main())

'''
loop = asyncio.get_event_loop()
loop.create_task(zmq_sub())
loop.create_task(rs232_reader())
loop.run_forever()
'''
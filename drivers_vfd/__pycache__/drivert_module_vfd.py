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
from drvt_handler_sync_vfd import Handler_Sync
from drvt_zmq_sub_vfd import Zmq_Sub
from dataclass_sync_reader import Dataclass_Reader_Sync


#async def rs232_reader():
def getSyncHandler():
#def getSyncHandler():

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
    #port = '/dev/ttyUSB7'
    port = '/dev/ttyMXUSB4'
    name_measurement = 'test'
    baudrate=9600
    bytesize=serial.EIGHTBITS
    parity=serial.PARITY_NONE
    stopbits=serial.STOPBITS_TWO
    timeout=1 
    write_timeout=0
    xonxoff=False
    rtscts=False
    dsrdtr=False

    dataclass_async_reader = Dataclass_Reader_Sync(name_measurement,port,baudrate,bytesize,
                                                   parity,stopbits,timeout,write_timeout,xonxoff,rtscts,dsrdtr) 

    
    handler_sync = Handler_Sync(dataclass_async_reader)

    #self.
    #reader_async = Reader_Async(port,baudrate,bytesize,parity,stopbits,write_timeout,xonxoff,rtscts,dsrdtr)
    #handler_sync = getSyncHandler(port,baudrate,bytesize,parity,stopbits,
    #             timeout,write_timeout,xonxoff,rtscts,dsrdtr)

    #serial.Serial(port,baudrate,bytesize,parity,stopbits,timeout,write_timeout,xonxoff,rtscts,dsrdtr)

    print("Doing rs232_handler")
    #reader_async.reader()
    return handler_sync


#async def zmq_sub():
def getZmqSub(rs232_handler):

    #bind_to = "tcp://localhost:7002" 
    bind_to = "tcp://localhost:7001" 

    zmq_sub = Zmq_Sub(rs232_handler, bind_to) 

    print("Doing the zmq_sub")
    #asyncio.run(zmq_sub.subscribe())
    #zmq_sub.subscribe()
    return zmq_sub


async def main():
        tracemalloc.start()
        
        rs232_handler = getSyncHandler() 
        zmq_sub = getZmqSub(rs232_handler)      
        
        tasks = []
        #tasks.append(asyncio.create_task(rs232_reader.reader()))
        tasks.append(asyncio.create_task(zmq_sub.subscribe()))
        
        await asyncio.gather(*tasks)
        

asyncio.run(main())

'''
loop = asyncio.get_event_loop()
loop.create_task(zmq_sub())
loop.create_task(rs232_reader())
loop.run_forever()
'''
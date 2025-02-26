'''

Модуль драйвера для работы с низкочастотным частотомером (Low Frequency Meter)
Выполняет следующие действия:
1. читает данные из прибора по порту RS232
2. записывает данные в БД
3. слушает данные с метками по zmq
4. записывает данные с метками в БД


'''
import asyncio
import os
import sys
import this
import tracemalloc
#import numpy
import zmq
import time
import random
import serial
import yaml

#from drv_zmq_sub_lfm import Reader_Async
from drvt_zmq_sub_lfm import Zmq_Sub
#from valeriy.projects.lotok.drivers.drv_reader_async_lfm import Reader_Async
from drvt_reader_async_lfm import Reader_Async
from dataclass_async_reader import Dataclass_Reader_Async


#async def rs232_reader():
def getAsyncReader(zmq_sub, port, name_measurement, divide_coef):
    #port = '/dev/ttyUSB5'
    #port = "/dev/ttyMXUSB3"
    port_test = "/dev/ttyMXUSB3"
    #port = '/dev/ttyMXUSB1'
    #port1 = '/dev/ttyMXUSB1'
    baudrate=9600
    bytesize=serial.EIGHTBITS
    parity=serial.PARITY_EVEN
    stopbits=serial.STOPBITS_ONE
    #timeout=0, #0.05
    write_timeout=0
    xonxoff=False
    rtscts=False
    dsrdtr=False
    dataclass_async_reader = Dataclass_Reader_Async(name_measurement,port,baudrate,divide_coef,bytesize,
    parity,stopbits,write_timeout,xonxoff,rtscts,dsrdtr)        

    reader_async = Reader_Async(zmq_sub, dataclass_async_reader)
    #reader_async = Reader_Async(name_measurement,port_test,baudrate,bytesize,parity,stopbits,write_timeout,xonxoff,rtscts,dsrdtr)

    print("Doing rs232_reader")
    #reader_async.reader()
    return reader_async


#async def zmq_sub():
def getZmqSub(name_measurement):

    bind_to = "tcp://localhost:7001" 
    #bind_to = "tcp://*:7001" 

    zmq_sub = Zmq_Sub(name_measurement, bind_to) 

    print("Doing the zmq_sub")
    #asyncio.run(zmq_sub.subscribe())
    #zmq_sub.subscribe()
    return zmq_sub


async def main():
        tracemalloc.start()

        print("Current working directory:", os.getcwd())
        #file_path = os.path.join(os.getcwd(), 'valeriy/projects/lotok/drivers')
        #file_path = os.path.join(os.getcwd(), 'lotok/drivers')
        #file_path = os.path.join(os.getcwd(), 'lotok/drivers/drivers_vfd')
        file_path = os.path.join(os.getcwd(), 'drivers/drivers_vfd')

        yml_file_path = os.path.join(file_path, 'lotok.yml')
        #print("file_path:", file_path)
        #list_dir0 = os.listdir(os.getcwd())
        #print("list_dir0:", list_dir0)


        if len (sys.argv) == 1:
            print ("Помилка! Відсутній параметр командного рядка")
            sys.exit (1)
        else:
            measure_param = sys.argv[1]
            

        with open(yml_file_path, 'r') as file:
            config = yaml.safe_load(file)

        port = config[measure_param]['rs232_port']
        name_measurement = config[measure_param]['name_measurement']  
        divide_coef = config[measure_param]['divide_coef']         
        
        zmq_sub = getZmqSub(name_measurement) 
        rs232_reader = getAsyncReader(zmq_sub, port, name_measurement, divide_coef)              
        
        tasks = []
        #tasks.append(asyncio.create_task(rs232_reader.reader_lfm()))
        tasks.append(asyncio.create_task(zmq_sub.subscribe()))
        tasks.append(asyncio.create_task(rs232_reader.reader_lfm()))
        
        await asyncio.gather(*tasks)
        

asyncio.run(main())

'''
loop = asyncio.get_event_loop()
loop.create_task(zmq_sub())
loop.create_task(rs232_reader())
loop.run_forever()
'''
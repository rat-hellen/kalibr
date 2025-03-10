#!/usr/bin/python3
'''
Драйвер для чтения в асинхронном режиме для тестов

'''
__author__ = 'UKRGMC'

import asyncio
from datetime import datetime
import binascii
#from asyncio import get_event_loop
from serial_asyncio import open_serial_connection
import random
#import openpyxl
import serial
from label_lowfreq_meter import Label_LowFreqMeter

from drv_db_client import Db_Client
#import time


#definition of the class starts here 
class Reader_Async: 
    #initializing the variables 
    #port = '/dev/ttyUSB5'
    port = '/dev/ttyMXUSB1'
    name_measurement = 'test'    
    baudrate = 9600
    divide_coef = 1
    bytesize=serial.EIGHTBITS
    parity=serial.PARITY_EVEN
    stopbits=serial.STOPBITS_ONE
    #timeout=0, #0.05
    write_timeout=0
    xonxoff=False
    rtscts=False
    dsrdtr=False
    
    
    #Label_LowFreqMeter lastSubReadLabel_lfm
   
    #defining constructor 
    def __init__(self, name_measurement_= name_measurement, port_=port,baudrate_=baudrate,divide_coef_=divide_coef,bytesize_=bytesize,
                 parity_=parity, stopbits_=stopbits,write_timeout_=write_timeout,xonxoff_=xonxoff,rtscts_=rtscts,dsrdtr_=dsrdtr): 
        self.name_measurement = name_measurement_
        self.port = port_
        self.baudrate=baudrate_
        self.divide_coef = divide_coef_
        self.bytesize=bytesize_
        self.parity=parity_
        self.stopbits=stopbits_
        #timeout=0, #0.05
        self.write_timeout=0
        self.xonxoff=xonxoff_
        self.rtscts=rtscts_
        self.dsrdtr=dsrdtr_ 
        self.canWriteToDB=False
        self.lastReadLine = ''

        #self.lastSubReadLabel_lfm
        print('self.port = ',self.port ,'  ASYNC READER')



    #defining class methods 
    # 
    def getDbClient(self):
        url = "tcp://localhost:7001" 
        dbase_name = 'lotok' 

        #db_client = Db_Client(url,dbase_name)
        db_client = Db_Client()

        print("Doing db_client")
        
        return db_client


    async def reader_lfm(self):
        '''
        Осуществляет чтение из серийного порта (указан в конструкторе) 
        и  первичную обработку строк низкочастотного частотомера
        '''
        reader, writer = await open_serial_connection(
            
        url=self.port,
        baudrate=self.baudrate,
        bytesize=self.bytesize,
        parity=self.parity,
        stopbits=self.stopbits,
        #timeout=0, #0.05,
        write_timeout=self.write_timeout,
        xonxoff=self.xonxoff,
        rtscts=self.rtscts,
        dsrdtr=self.dsrdtr)  


        while True:
            #print('reader_lfm : self.canWriteToDB= ', self.canWriteToDB)
            flag = await reader.read(1)
            #print(datetime.now().isoformat(),'!',flag)
            #b'A000000\x00\x90.
            #line_10 = b''
            if flag == b'/':
                line_10 = b''
                while len(line_10)<10:
                    line_10 += await reader.read(10-len(line_10))
                    
                #print('line_10 = ',line_10)
                
                
                if (self.canWriteToDB == True):
                    
                    await self.writeToDB(self.name_measurement, self.lastSubReadLabel_lfm, self.getFrequency())

                    #await self.writeToDB(line_10, str(line_10)[3:9])
                    print('line_10 = ',line_10,'  WRITTEN!')
                
                self.lastReadLine = line_10    
                #print(datetime.now().isoformat(),'  AR-->  ',line_10)

    

    def getFrequency(self):

        if (self.lastReadLine.strip() != ''):
            print('self.lastReadLine = ',self.lastReadLine)

            '''
            value09 = str(self.lastReadLine)[0:9]
            print('value09 = ',value09)
            value913 = str(self.lastReadLine)[9:13]
            print('value913 = ',value913)
            value1320 = str(self.lastReadLine)[13:20]
            print('value1320 = ',value1320)            
            '''
            #value1 = str(self.lastReadLine)[4:9]            
            value = float(str(self.lastReadLine)[4:9])
            #print('value = ',value)
            #order1 = str(self.lastReadLine)[11:13] 
            order = float(str(self.lastReadLine)[11:13])
            #print('order = ',order)

            if (order==2):
                freq_value = value/100
            else:
                if (order==3):
                    freq_value = value/1000
                else: freq_value = 0.0
            
        else: freq_value = 0.0

        freq_value = freq_value/self.divide_coef

        #print('freq_value = ',freq_value)

        return freq_value

    def setCanWriteToDB(self, flag):
        self.canWriteToDB = flag

    def setLastSubReadLabel_lfm(self, label_lfm):
        print('setLastSubReadLabel_lfm --> ',label_lfm)

        self.lastSubReadLabel_lfm = label_lfm
        print('setLastSubReadLabel_lfm SET!!! ')

            
    async def writeToDB(self, name_measurement, label_lfm, freq_value):
        '''
        Осуществляет первичную обработку строки с меткой и
        дальнейшую запись в БД 

        label_lfm - 

        '''
        #print('drv_reader_async: writeToDB --> ',data_line ,' ||  ',value)
        db_client = self.getDbClient()        
        
        #await db_client.write_data_lfm(data_line, value)
        await db_client.write_label_lfm(name_measurement, label_lfm, freq_value)  
        #await db_client.write_data_lfm(data_line, value)

            
            
               

    
              

       
       
    #end of the class definition 


#set = []

'''
[606143.697645] usb 1-6: Moschip 7840/7820 USB Serial Driver converter now attached to ttyUSB0
[606143.708047] usb 1-6: Moschip 7840/7820 USB Serial Driver converter now attached to ttyUSB1
[606143.708656] usb 1-6: Moschip 7840/7820 USB Serial Driver converter now attached to ttyUSB2
[606143.709291] usb 1-6: Moschip 7840/7820 USB Serial Driver converter now attached to ttyUSB3
[606166.234697] usb 1-5: FTDI USB Serial Device converter now attached to ttyUSB4
[606166.236343] usb 1-5: FTDI USB Serial Device converter now attached to ttyUSB5
[606166.237841] usb 1-5: FTDI USB Serial Device converter now attached to ttyUSB6
[606166.239290] usb 1-5: FTDI USB Serial Device converter now attached to ttyUSB7
'''


'''
loop = asyncio.get_event_loop()
loop.run_until_complete(reader())
loop.close()
'''




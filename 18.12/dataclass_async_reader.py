__author__ = 'UKRGMC'

#import asyncio
from datetime import datetime
#import binascii
#from asyncio import get_event_loop
from serial_asyncio import open_serial_connection
#import random
#import openpyxl
import serial
#from label_lowfreq_meter import Label_LowFreqMeter

#from drv_db_client import Db_Client
#import time



#definition of the class starts here 
class Dataclass_Reader_Async: 
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
        #self.canWriteToDB=False
        #self.lastReadLine = ''

    def getName_measurement(self):
        return self.name_measurement

    def getPort(self):
        return self.port

    def getBaudrate(self):
        return self.baudrate

    def getDivide_coef(self):
        return self.divide_coef

    def getBytesize(self):
        return self.bytesize

    def getParity(self):
        return self.parity

    def getStopbits(self):
        return self.stopbits

    def getWrite_timeout(self):
        return self.write_timeout

    def getXonxoff(self):
        return self.xonxoff

    def getRtscts(self):
        return self.rtscts

    def getDsrdtr(self):
        return self.dsrdtr

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
#import time

set = []
#config_file = openpyxl.load_workbook(filename='set/set_port_f.xlsx', data_only=True)
#config_file = openpyxl.load_workbook(filename='C://Users/Meteo/Desktop/Gen_3-500/set/set_port_f.xlsx', data_only=True)
#sheet_stats = config_file['1']

#if sheet_stats.cell(row=1, column=2).value != None: 
#    port = sheet_stats.cell(row=1, column=2).value
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

port = '/dev/ttyUSB5'
#ser = None

async def reader():
    '''
    Осуществляет чтение из серийного порта и первичную обработку строк
    '''
    reader, writer = await open_serial_connection(
        url=port,
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        #timeout=0, #0.05,
        write_timeout=0,
        xonxoff=False,
        rtscts=False,
        dsrdtr=False)  

    while True:
        #await asyncio.sleep(random.randint(1, 3))
        #print(datetime.now().isoformat(), '-!!!-')
        #print(datetime.now().isoformat(), reader.__str__)
        #reader.resume_reading()

        #line = await reader.readline()
        

        '''
        line_10 = await reader.read(25)
        print(datetime.now().isoformat(), "line_10 = " + str(line_10))
        #ans_pack = str(binascii.hexlify(ans_10[1:7]))
        param = float(line_10[2:8])
        #print(datetime.now().isoformat(), ans_10, ans_10[1:7], f, f/1000, 'Hz')
        print(datetime.now().isoformat(), line_10, param/1000, 'Hz')
        '''



        #print(datetime.now().isoformat(), line)

        #flag = line[0]
        flag = await reader.read(1)
        #print(datetime.now().isoformat(), "flag = " + str(flag))
        
        #ans_pack = str(binascii.hexlify(ans))
        #print(datetime.now().isoformat(), ans)

        
        if flag == b'/':
            line_10 = await reader.read(15)
            print(datetime.now().isoformat(), "line_10 = " + str(line_10))
            #ans_pack = str(binascii.hexlify(ans_10[1:7]))
            param = float(line_10[1:7])
            #print(datetime.now().isoformat(), ans_10, ans_10[1:7], f, f/1000, 'Hz')
            print(datetime.now().isoformat(), line_10, param/1000, 'Hz')
        



loop = asyncio.get_event_loop()
loop.run_until_complete(reader())
loop.close()






"""
try:
    ser = serial.Serial(
    port=port,
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    #timeout=3, #0.05,
    write_timeout=0,
    xonxoff=False,
    rtscts=False,
    dsrdtr=False)
except:
    print(
'Порт '+ port + ' не хочет открываться, может его нету в системе?\n\
Проверьте имя порта в файле \"set/set_port_f.xlsx\"\nПервая строка, вторая колонка!')
    while True:pass
else:
    print('Порт '+ port + ' открыт')
"""



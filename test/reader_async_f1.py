#!/usr/bin/python3
__author__ = 'UKRGMC'

import asyncio
from datetime import datetime
from serial_asyncio import open_serial_connection
import serial

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
async def reader():
    reader, writer = await open_serial_connection(
        url=port,
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        xonxoff=False,
        rtscts=False,
        dsrdtr=False)  

    while True:
        flag = await reader.read(1)
        print(datetime.now().isoformat(),'!',flag)
        if flag == b'/':
            line_10 = b''
            while len(line_10)<10:
                line_10 += await reader.read(10-len(line_10))
            print(datetime.now().isoformat(),'>',line_10)

loop = asyncio.get_event_loop()
loop.run_until_complete(reader())
loop.close()


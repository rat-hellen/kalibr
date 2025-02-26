#!/usr/bin/python3
__author__ = 'UKRGMC'

from datetime import datetime
import binascii
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

port = '/dev/ttyMXUSB3'
ser = None
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
    print('Порт '+ port + ' не хочет открываться, может нету в системе?')
else:
    print('Порт '+ port + ' открыт')

while ser!=None:
    try:
        ans = ser.read(1)
    except:
        print('except ser.read(1)')
        continue
    #ans_pack = str(binascii.hexlify(ans))
    #print(datetime.now().isoformat(), ans)
    if ans == b'/':
        ans_10 = ser.read(10)
        #ans_pack = str(binascii.hexlify(ans_10[1:7]))
        try:
            f = float(ans_10[1:7])
        except:
            print('except float(ans_10[1:7])')
            continue
        #print(datetime.now().isoformat(), ans_10, ans_10[1:7], f, f/1000, 'Hz')
        d = 1000
        #print(ans_10, hex(ans_10[7]))
        if ans_10[7]==2:
            d = 100
        if ans_10[7]==0xff:
            f=0.0
        str_f = '%.3f'%float(f/d)
        print(datetime.now().isoformat(), ans_10, '{:>10}'.format(str_f), 'Hz optic')


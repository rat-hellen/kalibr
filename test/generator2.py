#!/usr/bin/python3
__author__ = 'UKRGMC'


#icpdas.com 
#usb2514 to serial rs232
#I-756x_I-756xU-linux-manual.pdf
#If kernel version 3.12.0 and above:
#modprobe ftdi_sio
#echo 1b5c 0104 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id (VID) (PID)
#"/dev/ttyUSB0-3"

#import openpyxl
import asyncio
import serial_asyncio

import serial
import time

set = []
#config_file = openpyxl.load_workbook(filename='set/set_port_f.xlsx', data_only=True)
#config_file = openpyxl.load_workbook(filename='C://Users/Meteo/Desktop/Gen_3-500/set/set_port_f.xlsx', data_only=True)
#sheet_stats = config_file['1']
#sudo chmod a+rw /dev/ttyUSB0

#port = "/dev/ttyMXUSB1"
port = "/dev/ttyMXUSB2"
set = [{'f':1, 't':1000}]

records = []

#if sheet_stats.cell(row=1, column=1).value != None: 
    #port = sheet_stats.cell(row=1, column=1).value

'''    
for i in range(2, sheet_stats.max_row+1):
    f = 0.0
    t = 600
    if sheet_stats.cell(row=i, column=1).value != None: 
        f = float(sheet_stats.cell(row=i, column=1).value)
    if sheet_stats.cell(row=i, column=2).value != None: 
        t = float(sheet_stats.cell(row=i, column=2).value)
    if f != 0.0:
        print(f,"Hz",t,"sec")
        set.append({'f':f, 't':t})
'''

try:
    ser = serial.Serial(
        port=port,
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        timeout=1,
        write_timeout=0,
        xonxoff=False,
        rtscts=False,
        dsrdtr=False)
except:
    file = open("/sys/bus/usb-serial/drivers/ftdi_sio/new_id","w")
    #echo '1b5c 0104' > /sys/bus/usb-serial/drivers/ftdi_sio/new_id (VID) (PID)
    file.write('1b5c 0104')
    file.close()
    print('Порт '+ port + ' не хочет открываться \n \
Идентификаторы конвертера usb2514 уже записаны. Перезапустите программу')

else:
    print('Порт '+ port + ' открыт')
    for s in set:
        starttime = time.time()
        #time_sleep = 1/(2*s['f'])
        time_sleep = 15
        print('pulse duration =', time_sleep, 's', s['f'], 'Hz', s['t'], 's')
        while True:
            #ser.write(b'/A0003611\xff.')
            #b'A000000\x00\x90.
            ser.write(b'/A000123\x02\x90.')
            print(b'/A000123\x02\x90. ')            
            ser.setDTR(True)
            time.sleep(time_sleep)
            ser.setDTR(False)
            time.sleep(time_sleep)

            ser.write(b'/A000456\x02\x90.')
            #b'A123456\x02\x90
            print(b'/A000456\x02\x90. ')            
            ser.setDTR(True)
            time.sleep(time_sleep)
            ser.setDTR(False)
            time.sleep(time_sleep)

            ser.write(b'/A000789\x02\x90.')
            print(b'/A000789\x02\x90. ')            
            ser.setDTR(True)
            time.sleep(time_sleep)
            ser.setDTR(False)
            time.sleep(time_sleep)

            ser.write(b'/A011122\x03\x90.')
            print(b'/A011122\x03\x90. ')            
            ser.setDTR(True)
            time.sleep(time_sleep)
            ser.setDTR(False)
            time.sleep(time_sleep)

            ser.write(b'/A023456\x03\x90.')
            print(b'/A023456\x03\x90.')            
            
            ser.setDTR(True)
            time.sleep(time_sleep)
            ser.setDTR(False)
            time.sleep(time_sleep)
            

            

    #time.sleep(1000)

'''
    OptSensor:=OpticSensor.Create(PortOPT,
                                  false,
                                  CBR_300,
                                  ONESTOPBIT,
                                  EVENPARITY);
'''
import serial
import binascii
import time
import zmq
import crc_vfd_ascii
import pytz
import datetime
from datetime import datetime

bind_to = "tcp://*:7001" 
ctx = zmq.Context()
s = ctx.socket(zmq.PUB)
s.bind(bind_to)
print(datetime.now().isoformat(), '---START---')
time.sleep(10)

current_time = datetime.now()
start_time = str(current_time.hour)+':'+str(current_time.minute)+':'+str(current_time.second)
print('start_time',start_time)
serial_name = '55_test'
fn_name = '55_test'

for i in range(3):
    V='3.0'
    print(datetime.now().isoformat(), V)
    s.send_json({'SN': serial_name, 'FN': fn_name, 'V':V, 'VF':V, 'UNIT':'Hz', 'VO':'False', 'Start':start_time})
    time.sleep(10)
    V='5.0'
    print(datetime.now().isoformat(), V)
    s.send_json({'SN': serial_name, 'FN': fn_name, 'V':V, 'VF':V, 'UNIT':'Hz', 'VO':'False', 'Start':start_time})
    time.sleep(10)

s.send_json({'SN':'','FN':'','V':'','VF':'','UNIT':'','VO':'', 'Start':start_time})

print(datetime.now().isoformat(), '---EXIT---')

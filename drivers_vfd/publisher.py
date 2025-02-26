import serial
import binascii
import time
import zmq
import crc_vfd_ascii
import pytz
import datetime
from datetime import datetime

#bucket = "lotok"
#org = "gcto"
#token = "Ry1TrnhPAD2EwA_DahdVNIUXk2mYVZsWYu0PrB5KI6gYcFtsuVSMCKKy9IB7bgD7pUOOM1etx3ayjiDdEzz2Gw=="
#url = "http://localhost:8087"

#клиент influx:
#docker exec -it influx2 influx ...
#docker exec -it influx2 influx delete --bucket lotok --org gcto --start 2023-12-01T00:00:00Z --stop 2023-12-13T20:00:00Z --predicate '_measurement="vfd"'


#/bin/python /home/user/projects/lotok/drivers/drivert_module_vfd.py
#sudo scp -r /home/valeriy/projects/lotok/drivers /home/user/projects/lotok/drivers/last_valeriy
#rm -r /home/user/projects/lotok/drivers/last_valeriy
#/home/valeriy/projects/lotok/drivers/
#cQe7SUfp4sQTpC

#dmesg | grep tty
#dmesg | grep -i serial
#dmesg | grep -i FTDI
#ll /dev/tty*

# переименовывание портов моксы
#find /sys -name bComPreserver_com
#echo 4 > /sys/devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0/ttyUSB3/bComPreserver_com
#echo 3 > /sys/devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0/ttyUSB2/bComPreserver_com
#echo 2 > /sys/devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0/ttyUSB1/bComPreserver_com
#echo 1 > /sys/devices/pci0000:00/0000:00:14.0/usb1/1-3/1-3:1.0/ttyUSB0/bComPreserver_com

# установка vscode
#sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
#printf "[vscode]\nname=packages.microsoft.com\nbaseurl=https://packages.microsoft.com/yumrepos/vscode/\nenabled=1\ngpgcheck=1\nrepo_gpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc\nmetadata_expire=1h" | sudo tee -a /etc/yum.repos.d/vscode.repo
#sudo dnf install code -y

#dnf install python3-pip
#dnf install python3-pyserial

#dnf install zeromq-devel -- 
#dnf install uwsgi-emperor-zeromq --

#pip install pyserial
#pip install pyserial_asyncio
#pip install influxdb_client
#pip install pyzmq
#pip install openpyxl

#sudo usermod -a -G dialout user
#sudo usermod -a -G dialout valeriy

#port = '/dev/ttyMXUSB1'
#port = '/dev/ttyMXUSB2'
#port = '/dev/ttyMXUSB3'
#port = '/dev/ttyMXUSB4'

'''
serial_port_vfd = None
name_port = '/dev/ttyMXUSB4'
try:
    serial_port_vfd = serial.Serial(
    port=name_port,
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    timeout=5, 
    write_timeout=0,
    xonxoff=False,
    rtscts=False,
    dsrdtr=False)
except:
    print('Serial_port_VFD', name_port, 'No Open')
else:
    print('Serial_port_VFD', name_port, 'Open')
'''

bind_to = "tcp://*:7001" 
ctx = zmq.Context()
s = ctx.socket(zmq.PUB)
s.bind(bind_to)


###ret::::  b':01860475\r\n'

'''
def SendCommand06(addr,data):
    buffer = b':0106'+ addr + data
    cs = crc_vfd_ascii.lrc(buffer)
    buffer+= cs + b'\r\n'
    #print(buffer)
    serial_port_vfd.write(buffer)
    d = serial_port_vfd.read(17)
    print('ret:::: ',d)
'''

'''
#Код команды: 08H: проверка связи в сети между ведущим (ПК, ПЛК) и ведомыми
#(ПЧ) устройствами. Ведомый должен вернуть сообщение отправленное ведущим.
def SendCommand08():
    buffer = b':01080000177070\r\n'
    serial_port_vfd.write(buffer)
    d = serial_port_vfd.read(17)
    print('ret:',d)
'''

'''
    // Ответ:
    ReadEnd := ReadFile(hCom,Buffer,17,Readed,nil);
    if ReadEnd = FALSE then begin
        if  Readed=11 then begin
        // VFD  прислал исключение:
            if  ((Buffer[3]=byte('8')) and (Buffer[4]=byte('6'))) then begin
            VFD_Ret_Error:= (Buffer[5]-byte('0'))*10+(Buffer[6]-byte('0'));
            Application.MessageBox(
            Pchar('Код ошибки = '+IntToStr(VFD_Ret_Error)),
                //RetError[VFD_Ret_Error-1],
            'Ответ-исключение на команду 06',
            MB_ICONERROR);
            end;
        end;
'''
'''
def SetFrequency (Frequency):
    data = round(Frequency*100).to_bytes(2,'big')
    b_data = binascii.hexlify(data).upper()
    print('F set:', b_data, Frequency)
    SendCommand06(b'2001',b_data)

def Stop():
    SendCommand06(b'2000',b'0001')
def Run():
    SendCommand06(b'2000',b'0002')
def RunJog():
    SendCommand06(b'2000',b'0003')
def FWD():
    SendCommand06(b'2000',b'1000')
def REV():
    SendCommand06(b'2000',b'2000')

def init():
    #Источник задания выходной частоты
    #addr  $0200
    #data  $0004 : Интерфейс RS-485
    print('SendCommand06(0200,0004) Интерфейс RS-485')
    SendCommand06(b'0200',b'0004')
    #Источник управления приводом
    #addr  $0201
    #data  $0003 : Последовательный интерфейс RS-485, с
    #возможностью остановки привода кнопкой STOP
    print('SendCommand06(0201,0003) Последовательный интерфейс RS-485, c возможностью остановки привода кнопкой STOP')
    SendCommand06(b'0201',b'0003')

    #print('SendCommand08')
    #SendCommand08()

    #устанавливаем частоту не ноль (при нулевой частоте команда Run не выполняется)
    print('устанавливаем частоту 0.01, при нулевой частоте команда Run не выполняется!')
    SendCommand06(b'2001',b'0001')
    print('FWD:')
    FWD()
    print('Run')
    Run()

def exit():
    print('даем команду стоп')
    Stop()
    print('устанавливаем частоту ноль...')
    SendCommand06(b'2001',b'0000')
    print('возвращаем мастер-частоту...')
    SendCommand06(b'2000',b'0000')
    #Источник задания выходной частоты
    #addr  $0200
    #data  $0000 : Ведущая частота задается с цифровой панели управления или от
    #многофункциональных дискретных входов (UP/DOWN);
    print('Ведущая частота задается с цифровой панели управления... 0200:0000')
    SendCommand06(b'0200',b'0000')
    print('Управление от цифровой панели управления... 0201:0000')
    SendCommand06(b'0201',b'0000')
'''

#if serial_port_vfd != None:

#print('---START---')
#init()

#print('SetFrequency:')
#SetFrequency(3)
#time.sleep(10)

#utc_now = pytz.utc.localize(datetime.datetime.utcnow())
#loc_start = utc_now.astimezone(pytz.timezone("Europe/Kyiv"))
#print(loc_start.isoformat())
print(datetime.now().isoformat(), '---START---')

#s.send_json({'SN':'test', 'FN':'test', 'V':'0.35', 'UNIT':'Hz', 'VO':'False'})
#time.sleep(10)
#print('-Run-')
#Run()

#set = [0.81,0.90,1.20,1.80,2.40,3.00,3.90,4.80,6.00,7.20,9.00]
#for n in range(100):
    #f = 1.0 + 0.05*n

current_time = datetime.now()
start_time = str(current_time.hour)+':'+str(current_time.minute)+':'+str(current_time.second)
print('start_time',start_time)

'''
for n in range(80):
    f = 1.0 + 0.1*n
    V = '%.2f' %f
    #print('SetFrequency:', f)
    print(datetime.now().isoformat(), V)
    #serial = 'test_4'
    #fname = 'test_4'
    serial_name = '55_test'
    fn_name = '55_test'

    s.send_json({'SN': serial_name, 'FN': fn_name, 'V':V, 'VF':V, 'UNIT':'Hz', 'VO':'False', 'Start':start_time})
    #SetFrequency(f)
    time.sleep(15)
'''

serial_name = '55_test'
fn_name = '55_test'

V='1.5'
print(datetime.now().isoformat(), V)
s.send_json({'SN': serial_name, 'FN': fn_name, 'V':V, 'VF':V, 'UNIT':'Hz', 'VO':'False', 'Start':start_time})
time.sleep(30)
V='2.5'
print(datetime.now().isoformat(), V)
s.send_json({'SN': serial_name, 'FN': fn_name, 'V':V, 'VF':V, 'UNIT':'Hz', 'VO':'False', 'Start':start_time})
time.sleep(30)

#print('-exit-')
#exit()
#time.sleep(10)
s.send_json({'SN':'','FN':'','V':'','VF':'','UNIT':'','VO':'', 'Start':start_time})

print(datetime.now().isoformat(), '---EXIT---')
#utc_now = pytz.utc.localize(datetime.datetime.utcnow())
#loc_end = utc_now.astimezone(pytz.timezone("Europe/Kyiv"))
#print(loc_end.isoformat())

#частота 0.03Hz:
#SendCommand06(b'2001',3.2)
#str = 0x0d
#print(binascii.hexlify((b'\r')))

#Start = 'HHMMSS' 
'''
Scatter:
Auto Scale Domain

from(bucket: "lotok")
  |> range(start: 2023-12-15T00:00:00Z, stop: 2023-12-15T20:00:00Z)
  |> group()

from(bucket: "lotok")
  |> range(start: 2023-12-15T13:15:00Z, stop: 2023-12-15T13:40:00Z)
  |> filter(fn: (r) => r["_measurement"] == "vfd")
  |> group()

from(bucket: "lotok")
  |> range(start: 2023-12-15T12:00:00Z, stop: 2023-12-15T20:00:00Z)
  |> filter(fn: (r) => r["_measurement"] == "vfd")
  |> filter(fn: (r) => r["V"] == "1.10" or r["V"] == "1.20" or r["V"] == "1.30")
  |> group(columns: ["_time"]
  |> group()
'''
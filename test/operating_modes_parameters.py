import serial
import crc_vfd_ascii as crc_vfd_ascii
import yaml
import time

#with open("lotok.yaml", 'r') as stream:
#    data_loaded = yaml.safe_load(stream)
#    print(data_loaded)
#time.sleep(1000)

#excel_file = Workbook()
#excel_sheet = excel_file.create_sheet(title='VFD', index=0)

serial_port_vfd = None
port = '/dev/ttyMXUSB4'
try:
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
except:
    print('Serial_port_VFD', port, 'No Open')
else:
    print('Serial_port_VFD', port, 'Open')

def SendCommand03(addr,data):
    buffer = b':0103'+ addr + data
    cs = crc_vfd_ascii.lrc(buffer)
    buffer+= cs + b'\r\n'
    #print(buffer)

    serial_port_vfd.write(buffer)
    d = serial_port_vfd.read(17)
    print('ret:', d)
    return d

def read_par(addr,data):
    par = SendCommand03(addr,data)
    if par == b'': return 'Нет ответа'
    par = par.replace(b'\r\n',b'')
    #par = b'0103020203D1'
    par_hex = par[7:-2]
    dec = int(par_hex,16)
    return dec

print('-----------------------')
dec = read_par(b'0200',b'0001')
print('0200 Источник управления выходной частотой:')
if dec == 0:
    print('00 Ведущая частота задается с цифровой панели управления или от\r\n \
многофункциональных дискретных входов (UP/DOWN);')
if dec == 1:
    print('01 Ведущая частота задается с внешнего терминала AVI постоянным\r\n \
напряжением 0 … 10В (0…5В);')
if dec == 2:
    print('02 Ведущая частота задается с внешнего терминала ACI 1 постоянным током\r\n \
4 … 20мА;')
if dec == 3:
    print('03 Ведущая частота задается с внешнего терминала ACI 2 постоянным током\r\n \
4 … 20мА;')
if dec == 4:
    print('04 Ведущая частота задается с последовательного интерфейса RS-485.\r\n')
if dec == 5:
    print('05 Ведущая частота задается в соответствие с уставкой параметра 4-24.\r\n \
04-24:\r\n \
Сложение сигналов задания частоты\r\n \
Заводская уставка: 0\r\n \
Возможные значения: 00: нет сложения;\r\n \
01: AVI + ACI1;\r\n \
02: ACI1 + ACI2;\r\n \
03: AVI + ACI2;\r\n \
04: AVI + Мастер-частота с RS-485;\r\n \
05: ACI1 + Мастер-частота с RS-485;\r\n \
06: ACI2 + Мастер-частота с RS-485')

print('-----------------------')
dec = read_par(b'0201',b'0001')
print('0201 Источник управления режимами работы ПЧ:')
if dec == 0:
    print('00 Управление от цифровой панели управления;')
if dec == 1:
    print('01 Управление от внешних терминалов планки ДУ с активизацией клавиши\r\n \
STOP, расположенной на цифровой панели;')
if dec == 2:
    print('02 Управление от внешних терминалов планки ДУ с блокировкой клавиши\r\n \
STOP, расположенной на цифровой панели;')
if dec == 3:
    print('03 Управление от RS-485, с активизацией клавиши STOP, расположенной на\r\n \
цифровой панели;')
if dec == 4:
    print('04 Управление от RS-485, с блокировкой клавиши STOP,\r\n \
расположенной на цифровой панели.')

print('-----------------------')
dec = read_par(b'0202',b'0001')
print('0202 Способ остановки двигателя\r\n\
Этот параметр определяет способ остановки двигателя.\r\n\
после получения команды STOP и EF(внешняя ошибка)')
if dec == 0:
    print('00: STOP: остановка с замедлением выходной частоты за время установленное\r\n \
параметрами Pr.01-10 - Pr.01-16, EF: остановка на выбеге;')
if dec == 1:
    print('01: STOP: остановка с моментальным обесточиванием двигателя и замедлением\r\n \
на свободном выбеге, EF: остановка на выбеге;')
if dec == 2:
    print('STOP: остановка с замедлением, EF: остановка с замедлением;')
if dec == 3:
    print('STOP: остановка на выбеге, EF: остановка с замедлением.')


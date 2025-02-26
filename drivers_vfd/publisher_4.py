import time
import zmq
import datetime
from datetime import datetime

bind_to = "tcp://*:7001" 
ctx = zmq.Context()
s = ctx.socket(zmq.PUB)
s.bind(bind_to)
time.sleep(10)
print(datetime.now().isoformat(), '---START---')
current_time = datetime.now()
start = str(current_time.hour)+':'+str(current_time.minute)+':'+str(current_time.second)
print('Tag_Start', start)

f_set = [2.0,3.0]
for i in range(5):
    for f in f_set:
        V = '%.2f' %f
        print(datetime.now().isoformat(), V)
        s.send_json({'SN':'test_4', 'FN':'test_4', 'V':V, 'VF':V, 'UNIT':'Hz', 'VO':'False', 'Start':start})
        time.sleep(300)

    #for n in range(21):
        #f = 1.0 + 0.1*n #80
        #f = 1.0 + 0.1*n #21
        #f = 1.5 + 0.5*n #3
        #V = '%.2f' %f
        #print(datetime.now().isoformat(), V)
        #s.send_json({'SN':'test_4', 'FN':'test_4', 'V':V, 'VF':V, 'UNIT':'Hz', 'VO':'False', 'Start':start})
        #time.sleep(120)

    f = 0.01
    V = '%.2f' %f
    print(datetime.now().isoformat(), V)
    s.send_json({'SN':'test_4', 'FN':'test_4', 'V':V, 'VF':V, 'UNIT':'Hz', 'VO':'False', 'Start':start})
    time.sleep(60)

s.send_json({'SN':'','FN':'','V':'','VF':'','UNIT':'','VO':'', 'Start':start})
print(datetime.now().isoformat(), '---END---')


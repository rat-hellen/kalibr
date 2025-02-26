import time
import zmq

bind_to = "tcp://*:7001" 
ctx = zmq.Context()
s = ctx.socket(zmq.PUB)
s.bind(bind_to)
for i in range(10):
    s.send_json({'SN':'test','FN':'test','V':str((i+1)*0.1),'UNIT':'Hz','VO':'False'})
    time.sleep(180)
    s.send_json({'SN':'', 'FN':'', 'V':'', 'VO': ''})

import sys
#import numpy
import zmq
import time
import random

#bind_to = "/dev/ttyUSB5"
bind_to = "tcp://*:7001" 
#port = '/dev/ttyUSB5'
context = zmq.Context()
socket_pub = context.socket(zmq.PUB)
socket_pub.bind(bind_to)

print("Sending arrays...")
i=0

while True:

    '''
    zipcode = randrange(1, 100000)
    temperature = randrange(-80, 135)
    relhumidity = randrange(10, 60)
    '''
    serial = random.randrange(1111111, 9999999)
    velocity = round(random.uniform(0,20), 2)
    unit = random.choice(['Hz','m/c'])
    #random.randrange(0, 2000)/100
    velocity_overhead = random.choice([True, False])

    #serial_name = 'test'
    serial_name = '55-test'

    #socket_pub.send_string(f"{zipcode} {temperature} {relhumidity}")
    #string_for_sending = 'SN:' + str(serial) + '; FN:' + '' + '; V:'+ str(velocity) + '; VO:'+ str(velocity_overhead)
    string_for_sending = 'SN:' + serial_name + ', FN:' + 'test' + ', V:'+ str(velocity) + ', UNIT:'+ str(unit
    ) + ', VO:'+ str(velocity_overhead)
    socket_pub.send_json({'SN':'test', 'FN':'test', 'V':str(velocity), 'UNIT':str(unit)
    , 'VO':str(velocity_overhead)})

    print("Sended: " + string_for_sending)

    time.sleep(120)

    socket_pub.send_json({'SN':'test', 'FN':'test', 'V':str(velocity), 'UNIT':str(unit)
    , 'VO':str(velocity_overhead)})
    print("Sended: " + string_for_sending)
    time.sleep(120)

    socket_pub.send_json({'SN':'test', 'FN':'test', 'V':str(velocity), 'UNIT':str(unit)
    , 'VO':str(velocity_overhead)})
    print("Sended: " + string_for_sending)




    if (i==2):
        string_for_sending = 'SN:' + '' + '; FN:' + '' + '; V:'+ str(velocity) + '; VO:'+ str(velocity_overhead)
        socket_pub.send_json({'SN':'','FN':'','V':'','UNIT':'','VO':''})
        i=0
        print("Sended: " + string_for_sending)



    #socket_pub.send_string(string_for_sending)
    #s.send_json({'SN':'test', 'FN':'test', 'V':'0.3', 'UNIT':'Hz', 'VO': 'False'})
    i+=1

    #print("Sended: " + string_for_sending)

'''
def sync(bind_to: str) -> None:
    # use bind socket + 1
    sync_with = ':'.join(
        bind_to.split(':')[:-1] + [str(int(bind_to.split(':')[-1]) + 1)]
    )
    ctx = zmq.Context.instance()
    socket_rep = ctx.socket(zmq.REP)
    socket_rep.bind(sync_with)
    print("Waiting for subscriber to connect...")
    socket_rep.recv()
    print("   Done.")
    socket_rep.send(b'GO')


def main() -> None:    
   
    bind_to = "tcp://*:7001" 
    ctx = zmq.Context()
    socket_pub = ctx.socket(zmq.PUB)
    socket_pub.bind(bind_to)

    #sync(bind_to)

    print("Sending arrays...")
    for i in range(3):
        #a = numpy.random.rand(array_size, array_size)
        #s.send_pyobj(a)
        time.sleep(random.randint(1, 10))
        socket_pub.send_json({'SN':'5678990', 'V':'0.01', 'VO': 'False'})
    print("   Done.")


if __name__ == "__main__":
    main()
'''

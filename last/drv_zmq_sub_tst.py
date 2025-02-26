import sys
import zmq


#  Socket to talk to server
bind_to = "tcp://localhost:7001" 
#bind_to = "/dev/ttyUSB5"
#port = '/dev/ttyUSB5'

#tcp://localhost:5556
context = zmq.Context()
socket_sub = context.socket(zmq.SUB)

print("Collecting updates from server...")
socket_sub.connect(bind_to)

'''
zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10001"
socket_sub.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

serial, 'V':velocity, 'VO': velocity_overhead
'''
socket_sub.setsockopt_string(zmq.SUBSCRIBE, "")
#socket_sub.setsockopt(zmq.SUBSCRIBE)

# Process 5 updates
total_temp = 0
#for update_nbr in range(5):
while (True):
    print('Waiting for... ')
    string = socket_sub.recv_string()
    #serial, velocity, velocity_overhead = string.split()

    #total_temp += int(temperature)

    #print('Income data: SN:' + str(serial) + '; V: '+ str(velocity) + '; VO: '+ str(velocity_overhead))
    print('Received message : '+ string)
       
import sys
import numpy
import zmq
import time
import random

def sync(bind_to: str) -> None:
    # use bind socket + 1
    sync_with = ':'.join(
        bind_to.split(':')[:-1] + [str(int(bind_to.split(':')[-1]) + 1)]
    )
    ctx = zmq.Context.instance()
    s = ctx.socket(zmq.REP)
    s.bind(sync_with)
    print("Waiting for subscriber to connect...")
    s.recv()
    print("   Done.")
    s.send(b'GO')


def main() -> None:
    '''
    if len(sys.argv) != 4:
        print('usage: publisher <bind-to> <array-size> <array-count>')
        sys.exit(1)

    try:
        bind_to = "tcp://*:7001" #sys.argv[1]
        array_size = 3 #int(sys.argv[2])
        array_count = 2 #int(sys.argv[3])
    except (ValueError, OverflowError) as e:
        print('array-size and array-count must be integers')
        sys.exit(1)
    '''
    bind_to = "tcp://*:7001" 
    ctx = zmq.Context()
    s = ctx.socket(zmq.PUB)
    s.bind(bind_to)

    #sync(bind_to)

    print("Sending arrays...")
    for i in range(3):
        #a = numpy.random.rand(array_size, array_size)
        #s.send_pyobj(a)
        time.sleep(random.randint(1, 10))
        s.send_json({'SN':'5678990', 'V':'0.01', 'VO': 'False'})
    print("   Done.")


if __name__ == "__main__":
    main()

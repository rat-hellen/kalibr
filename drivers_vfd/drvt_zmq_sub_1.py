import asyncio
import zmq
import zmq.asyncio
from zmq.asyncio import Context

class Zmq_Sub:
    def __init__(self, url='localhost', port='7001'):
        self.url = "tcp://{}:{}".format(url, port)
        self.ctx = Context.instance()

        # activate publishers / subscribers
        asyncio.get_event_loop().run_until_complete(asyncio.wait([
            self.recv_string(),
        ]))

    async def recv_string(self):
        sub = self.ctx.socket(zmq.SUB)
        sub.bind(self.url)
        sub.setsockopt(zmq.SUBSCRIBE, "")

        # keep listening to all published message on topic 'world'
        while True:
            msg = await sub.recv_multipart()
            # ERROR: WAITS FOREVER
            print('received: ', msg)

import asyncio
import sys
import zmq
import zmq.asyncio
from label_vfd import Label_VFD
from drv_db_client import Db_Client
#from label_lowfreq_meter import Label_LowFreqMeter


#definition of the class starts here 
class Zmq_Sub: 
    #initializing the variables 
    #bind_to = "tcp://localhost:7001" 
    bind_to = "tcp://localhost:7002" 
    
    #defining constructor 
    def __init__(self, async_reader, binding_=bind_to): 
        self.bind_to = binding_
        self.velocity = 0
        self.async_reader = async_reader
        

    #defining class methods
    
    def getDbClient(self):
        url = "tcp://localhost:7001" 
        dbase_name = 'lotok' 

        #db_client = Db_Client(url,dbase_name)
        db_client = Db_Client()

        print("Doing db_client")
        
        return db_client
    

    def decode_message_toLabelVFD(self, message):  
        '''
        преобразует принятую строку в объект Label_VFD
        '''      

        strstr = str(message)

        index = strstr.find("SN:")
        #print("strstr = "+strstr)

        if (index!=-1):
            serial = strstr[index+3:strstr.find(";")]
            substr = strstr[strstr.find(";")+1:]

        else: 
            serial=''
            substr = strstr

        index = substr.find("FN:")

        if (index!=-1):
            opername = strstr[index+3:strstr.find(";")]
            substr = strstr[strstr.find(";")+1:]

        else: 
            opername=''

        index = substr.find("V:")
       
        if (index!=-1):
            velocity = substr[index+2:substr.find(";")]
            substr = strstr[strstr.find(";")+1:]

        else: 
            velocity=''            

        
        label = Label_VFD(serial,opername,velocity)
        return label


    def decode_message_ToLabel(self, message):
        '''
        возможна некоторая логика в дальнейшем
        т.к. сейчас только 1 вид метки, все отправляется в decode_message_toLabelVFD
        '''

        decoded_msg = self.decode_message_toLabelVFD(message)

        return decoded_msg

    async def recv_string(self):
        #sub = self.ctx.socket(zmq.SUB)
        #sub.bind(self.url)
        #sub.setsockopt(zmq.SUBSCRIBE, "")
        #zmq.asyncio.Socket.recv_multipart()

        msg = await self.socket_sub.recv_multipart() 
        
        return msg[0]
      

    async def subscribe(self):
        '''
        Осуществляет прослушивание сообщений по порту, указанному в конструкторе 
        '''

        context = zmq.asyncio.Context()
        self.socket_sub = context.socket(zmq.SUB)

        print("Zmq_Sub:  Collecting updates from server...")
        self.socket_sub.connect(self.bind_to)
        
        self.socket_sub.setsockopt_string(zmq.SUBSCRIBE, "")
        #socket_sub.setsockopt(zmq.SUBSCRIBE)

        # activate publishers / subscribers
        '''
        asyncio.get_event_loop().run_until_complete(asyncio.wait([
            self.recv_string(),
        ]))
        '''

        db_client = self.getDbClient()        
        
        while (True):
            #print('Waiting for... ')

            msg = await self.recv_string()

            decoded_label = self.decode_message_ToLabel(msg)
            if (decoded_label.getVelocity != self.velocity) :
                self.velocity = decoded_label.getVelocity
                if (decoded_label.serial != '' or decoded_label.opername != ''):
                    await db_client.write_label_vfd(decoded_label)   
      

       
    #end of the class definition 



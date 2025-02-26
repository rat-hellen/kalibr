import asyncio
import sys
import zmq
import zmq.asyncio
from drvt_db_client import Db_Client
from labelt_lowfreq_meter import Label_LowFreqMeter


#definition of the class starts here 
class Zmq_Sub: 
    #initializing the variables 
    bind_to = "tcp://localhost:7001" 
    #bind_to = "tcp://localhost:7002" 
    
    #defining constructor 
    def __init__(self, name_measurement, binding_=bind_to): 
        self.name_measurement = name_measurement
        self.bind_to = binding_
        #self.async_reader = async_reader
        self.canWriteToDB = False
        self.lastReadLine = ''
        #self.canWriteToDB=False
        

    #defining class methods
    
    def getDbClient(self):
        url = "tcp://localhost:7001" 
        dbase_name = 'lotok' 

        #db_client = Db_Client(url,dbase_name)
        db_client = Db_Client()

        print("Doing db_client...")
        
        return db_client
    

    '''
    '
    def decode_message_toLabelLowFreqMeter(self, message):  

        #b'SN:test; FN:test; V:5.83; UNIT:m/c; VO:True'  
            

        strstr = str(message)
        #print("drv_zmq_sub_lfm: strstr = "+strstr)

        index = strstr.find("SN:")
        #print('drv_zmq_sub_lfm: index =',index,'#')
        

        if (index!=-1):
            serial = strstr[index+3:strstr.find(";")]
            substring = strstr[strstr.find(";")+1:]
            if (serial!=''):
                self.canWriteToDB=True
            #print('drv_zmq_sub_lfm: serial ='+ serial+'#')
            #print("drv_zmq_sub_lfm: substring ="+substring+'###')

        else: 
            serial=''
            substring = strstr
            #print('drv_zmq_sub_lfm: serial =', serial,'@@@')

        index = substring.find("FN:")
        #print('drv_zmq_sub_lfm: index =',index,'$')

        if (index!=-1):
            #opername = substr[index+3:strstr.find(";")]
            opername = substring[substring.find(":")+1:substring.find(";")]
            substring = substring[substring.find(";")+1:]
            if (opername!=''):
                self.canWriteToDB=True
            #print('drv_zmq_sub_lfm: opername ='+opername+'#')

        else: 
            opername=''

        if ((serial=='')&(opername=='')):
            #print('drv_zmq_sub_lfm: serial =', serial,'&&&&&&&&&&&&')
            self.canWriteToDB=False    
        

        #print("drv_zmq_sub_lfm: substring ="+substring+'###')
        index = substring.find("V:")
       
        if (index!=-1):
            velocity = substring[index+2:substring.find(";")]
            substring = substring[substring.find(";")+1:]
            #print('drv_zmq_sub_lfm: velocity1 =', velocity,'$')

        else: 
            velocity=''
            #print('drv_zmq_sub_lfm: velocity2 =', velocity,'$')
            # 

        index = substring.find("UNIT:")
       
        if (index!=-1):
            unit = substring[index+2:substring.find(";")]
            substring = substring[substring.find(";")+1:]
            #print('drv_zmq_sub_lfm: velocity1 =', velocity,'$')

        else: 
            unit=''
            #print('drv_zmq_sub_lfm: velocity2 =', velocity,'$')              

        vo = substring[substring.find("VO:")+3:-1]
        #print('vo =', vo,'$')
        #print('vo= '+vo)

        label = Label_LowFreqMeter(serial,opername,velocity, unit, vo)
        return label
        '''

    '''
    def is_message_for_lfm(self, message):
        strstr = str(message)
        #print("drv_zmq_sub_lfm: strstr = "+strstr)
        index = strstr.find("VF")
        if (index!=-1):
            return False
        else:
            return True
    '''

    def decode_json_message_toLabelLowFreqMeter(self, message):  
        '''
        преобразует принятую строку в объект Label_LowFreqMeter
        '''
        #b'{"SN": "test", "FN": "test", "V": "0.3", "UNIT": "Hz", "VO": "False"}'
            

        strstr = str(message)
        #print("drv_zmq_sub_lfm: strstr = "+strstr)

        index = strstr.find("SN")
        #print('drv_zmq_sub_lfm: index =',index,'#')
        

        if (index!=-1):
            serial = strstr[index+6:strstr.find(",")-1]
            substring = strstr[strstr.find(",")+1:]
            if (serial!=''):
                self.setCanWriteToDB(True)
            print('drv_zmq_sub_lfm: serial ='+ serial+'#')
            #print("drv_zmq_sub_lfm: substring ="+substring+'###')

        else: 
            serial=''
            substring = strstr
            #print('drv_zmq_sub_lfm: serial =', serial,'@@@')

        index = substring.find("FN")
        #print('drv_zmq_sub_lfm: index =',index,'$')

        if (index!=-1):
            #opername = substr[index+3:strstr.find(";")]
            opername = substring[substring.find(":")+3:substring.find(",")-1]
            substring = substring[substring.find(",")+1:]
            if (opername!=''):
                self.setCanWriteToDB(True)
            #print('drv_zmq_sub_lfm: opername ='+opername+'#')

        else: 
            opername=''

        if ((serial=='')&(opername=='')):
            print('self.canWriteToDB=False')
            self.setCanWriteToDB(False)
        

        #print("drv_zmq_sub_lfm: substring ="+substring+'###')
        index = substring.find("V")
       
        if (index!=-1):
            velocity = substring[index+5:substring.find(",")-1]
            substring = substring[substring.find(",")+1:]
            #print('drv_zmq_sub_lfm: velocity =', velocity,'$')

        else: 
            velocity=''
            #print('drv_zmq_sub_lfm: velocity2 =', velocity,'$')

        index = substring.find("UNIT")
       
        if (index!=-1):
            unit = substring[index+8:substring.find(",")-1]
            substring = substring[substring.find(",")+1:]
            #print('drv_zmq_sub_lfm: unit =', unit,'$')

        else: 
            unit=''
            #print('drv_zmq_sub_lfm: velocity2 =', velocity,'$')              

        vo = substring[substring.find("VO")+6:-3]
        #print('vo =', vo,'$')
        #print('vo= '+vo)

        label = Label_LowFreqMeter(serial,opername,velocity,unit,vo)
        return label

    '''
    def is_message_empty(self, message):

        strstr = str(message)

        return False
    '''

    def setCanWriteToDB(self, flag):
        self.canWriteToDB = flag

    def setLastSubReadLabel_lfm(self, label_lfm):
        print('setLastSubReadLabel_lfm --> ',label_lfm)

        self.lastSubReadLabel_lfm = label_lfm
        print('setLastSubReadLabel_lfm SET!!! ')


    def decode_message_ToLabel(self, message):
        '''
        возможна некоторая логика в дальнейшем
        т.к. сейчас только 1 вид метки, все отправляется в decode_message_LabelLowFreqMeter
        '''

        #decoded_msg = self.decode_message_toLabelLowFreqMeter(message)
        decoded_msg = self.decode_json_message_toLabelLowFreqMeter(message)

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

        string = ''

        
        self.socket_sub.setsockopt_string(zmq.SUBSCRIBE, "")
        #socket_sub.setsockopt(zmq.SUBSCRIBE)

        # activate publishers / subscribers
        '''
        asyncio.get_event_loop().run_until_complete(asyncio.wait([
            self.recv_string(),
        ]))
        '''

        #db_client = self.getDbClient()        
        
        while (True):
            print('Waiting for... ')

            msg = await self.recv_string()

            #print('drv_zmq_sub_lfm: msg =  ', msg)
            #if (self.lfm(msg) == True):

            decoded_label = self.decode_message_ToLabel(msg)
            self.setLastSubReadLabel_lfm(decoded_label)
            #print('drv_zmq_sub_lfm:  self.async_reader.getCanWriteToDB()== ',self.async_reader.getCanWriteToDB())

            '''
            if (self.canWriteToDB==True):
            print('drv_zmq_sub_lfm:  self.async_reader.getCanWriteToDB==True!!!')
            freq_value = self.async_reader.getFrequency()
            await db_client.write_label_lfm(decoded_label, freq_value)  
            ''' 
      

       
    #end of the class definition 


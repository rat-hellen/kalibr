import asyncio
import sys
import zmq
import zmq.asyncio
from labelt_vfd import Label_VFD
from drvt_db_client import Db_Client
#from label_lowfreq_meter import Label_LowFreqMeter
#from drv_zmq_sub_lfm import Zmq_Sub
from drvt_vfd_motor_sync import Vfd_Motor_Driver


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

    def getVfdMotorDriver(self):
        url = "tcp://localhost:7001" 
        dbase_name = 'lotok' 

        #db_client = Db_Client(url,dbase_name)
        vfd_motor_driver = Vfd_Motor_Driver()

        print("Doing vfd_motor_driver")
        
        return vfd_motor_driver

    def is_message_for_vfd(self, message):
        strstr = str(message)
        #print("drv_zmq_sub_lfm: strstr = "+strstr)
        index = strstr.find("VF")
        if (index!=-1):
            return True
        else:
            return False

    def decode_json_message_toLabelVFD(self, message):  
        '''
        преобразует принятую строку в объект Label_VFD
        '''
        #b'{"SN": "test", "FN": "test", "V": "0.3", "VF": "0.3", "UNIT": "Hz", "VO": "False"}'
            

        strstr = str(message)
        #print("drv_zmq_sub_lfm: strstr = "+strstr)

        index = strstr.find("SN")
        #print('drv_zmq_sub_lfm: index =',index,'#')
        

        if (index!=-1):
            serial = strstr[index+6:strstr.find(",")-1]
            substring = strstr[strstr.find(",")+1:]
            if (serial!=''):
                self.async_reader.setCanWriteToDB(True)
            #print('drv_zmq_sub_lfm: serial ='+ serial+'#')
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
                self.async_reader.setCanWriteToDB(True)
            #print('drv_zmq_sub_lfm: opername ='+opername+'#')

        else: 
            opername=''

        if ((serial=='')&(opername=='')):
            print('self.canWriteToDB=False')
            self.async_reader.setCanWriteToDB(False)
        

        #print("drv_zmq_sub_lfm: substring ="+substring+'###')
        index = substring.find("V")
       
        if (index!=-1):
            velocity = substring[index+5:substring.find(",")-1]
            substring = substring[substring.find(",")+1:]
            #print('drv_zmq_sub_lfm: velocity =', velocity,'$')

        else: 
            velocity=''
            #print('drv_zmq_sub_lfm: velocity2 =', velocity,'$')

        index = substring.find("VF")
        #print('drv_zmq_sub_lfm: substring1 =', substring,'$')
       
        if (index!=-1):
            #velocityFreq = substring[index+5:substring.find(",")-1]
            velocityFreq = substring[index+6:substring.find(",")-1]
            substring = substring[substring.find(",")+1:]
            #print('drv_zmq_sub_lfm: velocityFreq =', velocityFreq,'$')

        else: 
            velocityFreq=''
            #print('drv_zmq_sub_lfm: velocity2 =', velocity,'$')

        #print('drv_zmq_sub_lfm: substring2 =', substring,'$')
        index = substring.find("UNIT")
       
        if (index!=-1):
            #unit = substring[index+8:substring.find(",")-1]
            unit = substring[index+8:substring.find(",")-1]
            substring = substring[substring.find(",")+1:]
            #print('drv_zmq_sub_lfm: unit =', unit,'$')

        else: 
            unit=''
            #print('drv_zmq_sub_lfm: velocity2 =', velocity,'$')              

        vo = substring[substring.find("VO")+6:-3]
        #print('vo =', vo,'$')
        #print('vo= '+vo)

        #label = Label_LowFreqMeter(serial,opername,velocity,unit,vo)
        label = Label_VFD(serial,opername,velocity,velocityFreq,unit,vo)
        return label
    
    '''
    def decode_message_toLabelVFD(self, message):  
        
        #преобразует принятую строку в объект Label_VFD
              

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
        '''

    


    def decode_message_ToLabel(self, message):
        '''
        возможна некоторая логика в дальнейшем        
        '''

        decoded_msg = self.decode_json_message_toLabelVFD(message)
        #decoded_msg = Zmq_Sub.decode_json_message_toLabelLowFreqMeter(message)

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
        motor_driver = self.getVfdMotorDriver()      
        
        while (True):
            #print('Waiting for... ')

            msg = await self.recv_string()
            #print('msg = ',msg)

            if (self.is_message_for_vfd(msg) == True):
                #print('self.is_message_for_vfd(msg) == True ')

                decoded_label = self.decode_message_ToLabel(msg)
                #print('decoded_label = ',decoded_label)
                if (decoded_label.isHeaderEmpty()):
                    #print('decoded_label.isHeaderEmpty() ')
                    #stop motor
                    if motor_driver.isRun() == True:
                        #print('motor_driver.isRun() == True ')
                        motor_driver.exit()
                else:
                    #print('NOT decoded_label.isHeaderEmpty() ')
                    if motor_driver.isRun() == False:
                        #print('motor_driver.isRun() == False ')
                        motor_driver.Run()

                    #print('decoded_label.getUnit()= ',decoded_label.getUnit())

                    if (decoded_label.getUnit()=="Hz"):
                        #print('decoded_label.getUnit()=="Hz" ')
                        ###motor.setFrequency
                        frequency = decoded_label.getVelocityFreq()
                        if frequency == 0 :
                            frequency = 0.01
                        #print('frequency = ',frequency)
                        if (motor_driver.SetFrequency(frequency)!=''):
                            #TODO отримати підтвердження від мотора, що команда виконана
                            #TODO analyze response: what should it be like

                            if (decoded_label.isHeaderEmpty() == False):
                                #if (decoded_label.serial != '' or decoded_label.opername != ''):
                                await db_client.write_label_vfd(decoded_label) 


                    else:
                        if (decoded_label.getUnit()=="m/c"):
                            #TODO визначаємо з калібровочної характеристики, або таблиці яка
                            #частота відповідає цій швидкості  
                            velocityFreq = decoded_label.getVelocityFreq()                            
                            
                            if (decoded_label.getVelocity != self.velocity) :
                                self.velocity = decoded_label.getVelocity
                                if (decoded_label.isHeaderEmpty):
                                #if (decoded_label.serial != '' or decoded_label.opername != ''):
                                    await db_client.write_label_vfd(decoded_label) 
                                      
      

       
    #end of the class definition 


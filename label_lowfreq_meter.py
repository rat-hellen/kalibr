'''
Асинхронний прийом міток для бд по Zmq (json) :7001
SN - серійний номер датчика
FN -  ім’я фамілія оператора
V - задана швидкість (м/с)
VO (true, false) - чи досягнута задана швидкість


'''

#definition of the class starts here 
class Label_LowFreqMeter: 
    #initializing the variables 
    #bind_to = "tcp://localhost:7001" 
    url='http://localhost:8086'
    database='lotok'

    #defining constructor 
    def __init__(self, serial_, opername_, velocity_, unit_, vo_ ): 
        self.serial = serial_
        self.opername = opername_
        self.velocity = velocity_
        self.unit = unit_
        self.vo = vo_
        

    #defining class methods

    def getSerial(self):
                
        return self.serial

    def getOpername(self):
                
        return self.opername

    def getVelocity(self):
                
        return self.velocity

    def getUnit(self):

        return self.unit

    def getVo(self):
                
        return self.vo

    def isHeaderEmpty(self):
        return self.serial == '' and self.opername == ''

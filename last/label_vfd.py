'''
Асинхронний прийом міток  i команд для бд по Zmq (json) :7001
SN - серійний номер датчика (номер еталона якщо йде калібровка установки, або назва вимірювання для експерименту) 
FN -  ім’я фамілія оператора (або інженера, що проводить калібровку установки, тестовий експеримент)
V - задана швидкість (м/с або Hz) - якщо не змінилося значення, не дається команда для інвертора, не зберігається в бд 
решта опублікованих міток ігнорується цим модулем


'''

#definition of the class starts here 
class Label_VFD: 
    #initializing the variables 
    #bind_to = "tcp://localhost:7001" 
    url='http://localhost:8086'
    database='lotok'

    #defining constructor 
    def __init__(self, serial_, opername_, velocity_ ): 
        self.serial = serial_
        self.opername = opername_
        self.velocity = velocity_
        

    #defining class methods

    def getSerial(self):
                
        return self.serial

    def getOpername(self):
                
        return self.opername

    def getVelocity(self):
                
        return self.velocity

    def isHeaderEmpty(self):
        return self.serial == '' and self.opername == ''

 
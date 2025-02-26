#import influxdb_client
from influxdb_client import Point
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

#from drivers.labelt_lowfreq_meter import Label_LowFreqMeter
#from labelt_lowfreq_meter import Label_LowFreqMeter
from lotok.drivers.labelt_lowfreq_meter import Label_LowFreqMeter

from influxdb_client import InfluxDBClient


#definition of the class starts here 
class Db_Client: 
    #initializing the variables 
    #bind_to = "tcp://localhost:7001" 
    #url='http://localhost:8086'
    #database='lotok'

    bucket = "lotok"
    org = "gcto"
    token = "Ry1TrnhPAD2EwA_DahdVNIUXk2mYVZsWYu0PrB5KI6gYcFtsuVSMCKKy9IB7bgD7pUOOM1etx3ayjiDdEzz2Gw=="
    url = "http://localhost:8087"

    #defining constructor 
    def __init__(self, url_=url, token_=token, org_=org, bucket_=bucket): 
        self.url = url_
        self.token=token_
        self.org=org_
        self.bucket=bucket_
        self.client = InfluxDBClientAsync(url=self.url, token=self.token, org=self.org)


    #defining destructor 
    #def __del__(self):
        #self.client.close()
        

    #defining class methods

    async def connect(self):
        
        #client = InfluxDBClient(url=self.url, database=self.database)
        client = InfluxDBClientAsync(url=self.url, token=self.token, org=self.org)
        
        return client


    async def reader(self):
        '''
        Осуществляет чтение метки из базы данных
        '''

    async def read_currentSpeed(self, unit, sn) :
        '''
        Осуществляет чтение метки из базы данных
        Поточна швидкість/частота потоку, яку сервер прочитав з бд. Останнє значення.
        '''

        #TODO 1. change query 2. return only time + V?

        measurement = "testW"

        #queryT = 'from(bucket: "'+self.bucket+'") |> range(start: -1m)'
        clientS = InfluxDBClient(url=self.url, token=self.token, org=self.org)

        queryT = f'from(bucket: "'+self.bucket+'")' \
          '|> range(start: 0, stop: now())' \
          '|> filter(fn: (r) => r["_measurement"] == "'+measurement+'")' \
          '|> filter(fn: (r) => r["UNIT"] == "'+unit+'")' \
          '|> filter(fn: (r) => r["SN"] == "'+sn+'")' \
          '|> keep(columns: ["SN", "UNIT", "V", "_time", "_value"])' \
          '|> group()' \
          '|> sort(columns: ["_time"], desc: false)' \
          '|> last(column: "_time")' \
                 
      
        tables = clientS.query_api().query(queryT)  
        clientS.close()

        '''        
        #output = tables.to_values(columns=["SN", 'FN', 'V', 'UNIT', 'VO', '_time', '_value'])
        speed = tables[0].records[0]["V"]
        return speed
        '''
        return tables

    async def read_currentSensor(self, sn) :
        '''
        Осуществляет чтение метки из базы данных
        Поточна частота датчика, яку сервер прочитав з бд. Останнє значення.
        '''

        #TODO 1. change query 2. return only time + V?
        measurement = "testW"

        #queryT = 'from(bucket: "'+self.bucket+'") |> range(start: -1m)'
        clientS = InfluxDBClient(url=self.url, token=self.token, org=self.org)

        queryT = f'from(bucket: "'+self.bucket+'")' \
          '|> range(start: 0, stop: now())' \
          '|> filter(fn: (r) => r["_measurement"] == "'+measurement+'")' \
          '|> filter(fn: (r) => r["UNIT"] == "Hz")' \
          '|> filter(fn: (r) => r["SN"] == "'+sn+'")' \
          '|> keep(columns: ["SN", "UNIT", "V", "_time", "_value"])' \
          '|> group()' \
          '|> sort(columns: ["_time"], desc: false)' \
          '|> last(column: "_time")' \

        tables = clientS.query_api().query(queryT)        
        clientS.close()            

        return tables


    async def write_label_lfm(self, name_measurement, label_lfm, freq_value):
        '''
        Осуществляет запись метки в базу данных
        '''
        #print("drv_db_client: write_label_lfm")

        #client = await self.connect()

        ''' 

        dictionary = {
                    "name": "test",
                    "SN": label.getSerial(),
                    "FN": label.getOpername(),
                    "V": label.getVelocity(),
                    "VO": label.getVo(),
                    #"time": datetime.now().isoformat(),
                    "f": 0.05
                }
        point = Point.from_dict(dictionary,
                                        #write_precision=WritePrecision.S,
                                        record_measurement_key="name",
                                        record_time_key="time",
                                        record_tag_keys=["SN", "FN"],
                                        record_field_keys=["V", "VO", "f"])
        #await client.write_api().write(bucket=bucket, org=org, record=dictionary)
        print("Point = ",point)
        await client.write_api().write(bucket=self.bucket, record=point)
        '''

        p = Point(name_measurement).tag("SN", label_lfm.getSerial()).tag("FN", label_lfm.getOpername()).tag(
            "V", label_lfm.getVelocity()).tag("UNIT", label_lfm.getUnit()).tag("VO", label_lfm.getVo()
            ).field("f", freq_value)
        await self.client.write_api().write(bucket=self.bucket, record=p)

        #write_api = client.write_api(write_options=SYNCHRONOUS)
        #await client.write_api().write(bucket=self.bucket, record=json_body)
        #await client.close()

        """
        for test
        """
        
        
        queryT = 'from(bucket: "'+self.bucket+'") |> range(start: -1m)'

        clientS = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        tables = clientS.query_api().query(queryT)
        
        #print(tables._to_values)
        output = tables.to_values(columns=['SN', 'FN', 'V', 'VO', 'UNIT', '_time', '_value'])
        print(output)
        clientS.close()
       

        
              

        '''
        for result in tables:
            print(result) 
            '''
               

        '''

        # Query: using Table structure
        tables = await client.query_api().query('from(bucket: "'+self.bucket+'") |> range(start: -10m)')

        output = tables.to_values(columns=['location', '_time', '_value'])
                print(output)
        
        # Serialize to values
        output = tables.to_values()
        print(output)
        '''

        #await client.close()

    async def write_label_vfd(self, label_vfd):
        '''
        Осуществляет запись метки в базу данных
        '''
        #print("drv_db_client: write_label_vfd")
        
        #client = await self.connect()
        
        #p = Point("vfd").tag("SN", label_vfd.getSerial()).tag("FN", label_vfd.getOpername()).tag(
        #   "V", label_vfd.getVelocity())

        freq = float(label_vfd.getVelocityFreq())
        
        p = Point("vfd").tag("SN", label_vfd.getSerial()).tag("FN", label_vfd.getOpername()).tag(
            "V", label_vfd.getVelocity()).tag("UNIT", label_vfd.getUnit()).tag("VO", label_vfd.getVo()
            ).field("f", freq )
        
        
        await self.client.write_api().write(bucket=self.bucket, record=p)

        #await self.client.write_api().write(bucket=self.bucket, record=p)
        #await client.close()

        """
        for test
        """

        '''
        
        queryT = 'from(bucket: "'+self.bucket+'") |> range(start: -1m)'
        clientS = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        tables = clientS.query_api().query(queryT)

        #print(tables._to_values)
        output = tables.to_values(columns=['SN', 'FN', 'UNIT', 'V', 'VO','_time', '_value'])
        print(output)
        clientS.close()
        '''
        

    async def write_data_lfm(self, data_line, freq_value):
        '''
        каждый принятый по кому пакет записывает в базу. 
        '''

        #print("drv_db_client: write_data_lfm")
        #print("drv_db_client: freq_value ="+freq_value)


        try:
            value = float(freq_value)
        except ValueError:
            value = 0

        #print("drv_db_client: value =",value)

        
        #client = await self.connect()

        p = Point("test").tag("V", data_line).tag("time",datetime.now().isoformat()).field("f", value)
        await self.client.write_api().write(bucket=self.bucket, record=p)
        #await client.close()


              





              



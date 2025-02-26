import asyncio
import random
import time
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from influxdb_client import InfluxDBClient
from influxdb_client import Point
from datetime import datetime

bucket = "lotok"
org = "gcto"
token = "Ry1TrnhPAD2EwA_DahdVNIUXk2mYVZsWYu0PrB5KI6gYcFtsuVSMCKKy9IB7bgD7pUOOM1etx3ayjiDdEzz2Gw=="

url = "http://localhost:8087"
async def main():
    async with InfluxDBClientAsync(url=url, token=token, org=org) as client:

        sn = "56783412"
        names_list = ["Pivnenko", "Vantuh"]
        vo_list = ["True", "False"]
        unit_list = ["Hz", "m/c"]

        for x in range(12):
            fn = random.choice(names_list)
            velocity = round(random.uniform(2.5, 20.0),2) 
            vo = random.choice(vo_list)
            unit = random.choice(unit_list)
            freq = round(random.uniform(0.2, 10.0),2)

            p = Point("testW").tag("SN", sn).tag("FN", fn).tag(
            "V", velocity).tag("UNIT", unit).tag("VO", vo
            ).field("f", freq )
            time.sleep(1)

            print("****")
            print(p)

            #p = Point("test").tag("SN", sn).tag("FN", "Pivnenko").tag("V", "11.1").tag("VO", "True").field("f", 0.04)
            await client.write_api().write(bucket=bucket, record=p)

        p = Point("testW").tag("SN", sn).tag("FN", "Pivnenko").tag("V", "11.1").tag("UNIT", "Hz").tag("VO", "True").field("f", 0.56)
        await client.write_api().write(bucket=bucket, record=p)
        time.sleep(2)
        print("**** ***** *****")
        print(p)

        p = Point("testW").tag("SN", sn).tag("FN", "Vantuh").tag("V", "22.2").tag("UNIT", "m/c").tag("VO", "True").field("f", 0.45)
        await client.write_api().write(bucket=bucket, record=p)
        print("**** ***** *****")
        print(p)


        

        #print(tables._to_values)
        #output = tables.to_values(columns=['SN', 'FN', 'V', '_time', '_value'])
        #print(output)
        #tables = client.query_api().query(queryT)

        #output = tables.to_values(columns=['SN', 'FN', 'V', 'VO', '_time', '_value'])
        #print(output)


        


        
        '''
        dictionary = {
                    "measurement": "h2o_feet",
                    "tags": {"location": "us-west"},
                    "fields": {"level": 125},
                    "time": 1
                }
        '''
        dictionary = {
                    "name": "test",
                    "SN": "1203367",
                    "FN": "Vantuh",
                    "V": "17.2",
                    "VO": "False",
                    #"time": datetime.now().isoformat(),
                    "f": 0.04
                }
        point = Point.from_dict(dictionary,
                                        #write_precision=WritePrecision.S,
                                        record_measurement_key="name",
                                        record_time_key="time",
                                        record_tag_keys=["SN", "FN"],
                                        record_field_keys=["V", "VO", "f"])
        #await client.write_api().write(bucket=bucket, org=org, record=dictionary)
        #await client.write_api().write(bucket=bucket, org=org, record=point)
        #await client.write_api().write(bucket=bucket, record=point)

        clientS = InfluxDBClient(url=url, token=token, org=org)
        #queryT = 'from(bucket: "'+bucket+'") |> range(start: -1m)'
        
        queryT = f'from(bucket: "'+bucket+'")' \
          '|> range(start: 0, stop: now())' \
          '|> filter(fn: (r) => r["_measurement"] == "testW")' \
          '|> filter(fn: (r) => r["UNIT"] == "Hz")' \
          '|> keep(columns: ["SN", "UNIT", "V", "_time", "_value"])' \
          '|> group()' \
          '|> sort(columns: ["_time"], desc: false)' \
          '|> last(column: "_time")' \
          
        
        '''
        queryT = f'from(bucket: "'+bucket+'")' \
          '|> range(start: 0, stop: now())' \
          '|> filter(fn: (r) => r["_measurement"] == measurement)' \
          '|> sort(columns: ["_time"], desc: false)' \          
          '|> group()' \
          '|> last(column: "_time")' \
          '''


        tables = clientS.query_api().query(queryT)              
        
        output = tables.to_values(columns=["SN", 'FN', 'V', 'UNIT', 'VO', '_time', '_value'])
        print("***********")
        print(output)

        output2 = tables[0].records[0]
        #client.close()
        print("*****2******")
        print(output2) 

        output3 = tables[0].records[0]["V"]
        #client.close()
        print("******3*****")
        print(output3) 

        
        output4 = tables[0].records[0]["_value"] 
        #client.close()
        print("******4*****")        
        print(output4) 
        


        '''
        start = "1970-01-01T00:00:00Z"
        stop = "2023-06-01T18:00:00Z"
        delete_api = client.delete_api()
        await delete_api.delete(start, stop, '_measurement="test"', bucket=bucket, org=org)
        '''

if __name__ == "__main__":
    asyncio.run(main())


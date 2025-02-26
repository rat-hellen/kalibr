import asyncio
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
        p = Point("test").tag("SN", "1208987").tag("FN", "Pivnenko").tag("V", "11.1").tag(
            "VO", "True").field("f", 0.04)
        await client.write_api().write(bucket=bucket, record=p)
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
        queryT = 'from(bucket: "'+bucket+'") |> range(start: -1m)'
        tables = clientS.query_api().query(queryT)        
        
        output = tables.to_values(columns=['SN', 'FN', 'V', 'VO', '_time', '_value'])
        print(output)


        '''
        start = "1970-01-01T00:00:00Z"
        stop = "2023-06-01T18:00:00Z"
        delete_api = client.delete_api()
        await delete_api.delete(start, stop, '_measurement="test"', bucket=bucket, org=org)
        '''

if __name__ == "__main__":
    asyncio.run(main())


    '''
    p = Point("test").tag("SN", label.getSerial()).tag("FN", label.getOpername()).tag(
            "V", label.getVelocity()).tag("VO", label.getVo()).time(
                datetime.now().isoformat()).field("f", 0.05)


    # Use custom dictionary structure
                dictionary = {
                    "name": "sensor_pt859",
                    "location": "warehouse_125",
                    "version": "2021.06.05.5874",
                    "pressure": 125,
                    "temperature": 10,
                    "created": 1632208639,
                }
                point = Point.from_dict(dictionary,
                                        write_precision=WritePrecision.S,
                                        record_measurement_key="name",
                                        record_time_key="created",
                                        record_tag_keys=["location", "version"],
                                        record_field_keys=["pressure", "temperature"])



    # Record as Dictionary
                dictionary = {
                    "measurement": "h2o_feet",
                    "tags": {"location": "us-west"},
                    "fields": {"level": 125},
                    "time": 1
                }
                await write_api.write("my-bucket", "my-org", dictionary)
    
    
        json_body = [
            {
                "measurement": "test",
                "tags": {
                    "SN": label.getSerial(),
                    "FN": label.getOpername(),
                    "V":  label.getVelocity(),
                    "VO": label.getVo()
                },
                "time": datetime.now().isoformat(),
                "fields": {
                    "f": 0.05
                }
            }
        ] 
        '''
    
    
    
    

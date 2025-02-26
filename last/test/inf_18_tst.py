import influxdb_client
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

url='http://localhost:8086'
#client = InfluxDBClient(host='localhost', port=8086, database='lotok')
client = InfluxDBClient(url=url, database='lotok')
json_body = [
    {
        "measurement": "verified_sensor",
        "tags": {
            "SN": "12345",
            "V":"1.5",
            "VO":"false"
        },
        "time": datetime.now().isoformat(),
        "fields": {
            "f": 0.05
        }
    }
]   
write_api = client.write_api(write_options=SYNCHRONOUS)
write_api.write(json_body)


results = client.query("select * from verified_sensor limit 1")
measure = next(results.get_points('verified_sensor'))
if(measure):
    print(measure)

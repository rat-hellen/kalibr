import asyncio
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from influxdb_client import Point

bucket = "lotok"
org = "gcto"
token = "Ry1TrnhPAD2EwA_DahdVNIUXk2mYVZsWYu0PrB5KI6gYcFtsuVSMCKKy9IB7bgD7pUOOM1etx3ayjiDdEzz2Gw=="
url = "http://localhost:8087"
async def main():
    async with InfluxDBClientAsync(url=url, token=token, org=org) as client:
        p = Point("test_measurement").tag("location", "Prague").field("temperature", 22.7)
        await client.write_api().write(bucket=bucket, record=p)

if __name__ == "__main__":
    asyncio.run(main())

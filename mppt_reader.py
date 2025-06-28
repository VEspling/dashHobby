import asyncio, json
from bleak import BleakScanner

async def read_mppt():
    devices = await BleakScanner.discover()
    for d in devices:
        if "SmartSolar" in d.name:
            with open("status.json", "r") as f:
                try:
                    status = json.load(f)
                except:
                    status = {}
            status["mppt"] = d.name
            with open("status.json", "w") as f:
                json.dump(status, f, indent=2)
            return

asyncio.run(read_mppt())

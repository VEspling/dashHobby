import asyncio, json, sqlite3
from datetime import datetime
from bleak import BleakScanner

async def read_mppt():
    devices = await BleakScanner.discover()
    for d in devices:
        if "SmartSolar" in d.name:
            data = {
                "device": d.name,
                "address": d.address,
                "timestamp": datetime.utcnow().isoformat()
            }

            conn = sqlite3.connect("eink_data.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO mppt_data (data) VALUES (?)", [json.dumps(data)])
            conn.commit()
            conn.close()

            print(f"✅ MPPT-data sparad: {data}")
            return

asyncio.run(read_mppt())

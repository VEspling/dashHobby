# mppt_reader.py
import asyncio
import json
import time
from datetime import datetime
from bleak import BleakScanner

STATUS_FILE = "status.json"

def update_status(mppt_info):
    try:
        with open(STATUS_FILE, "r") as f:
            status = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        status = {}

    status["mppt"] = {
        "name": mppt_info["name"],
        "address": mppt_info["address"],
        "timestamp": datetime.now().isoformat()
    }

    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2)
    print(f"✅ MPPT info saved: {mppt_info['name']} @ {mppt_info['address']}")

async def read_mppt():
    print("🔍 Scanning for SmartSolar devices...")
    devices = await BleakScanner.discover(timeout=5.0)
    for d in devices:
        if d.name and "SmartSolar" in d.name:
            mppt_info = {
                "name": d.name,
                "address": d.address
            }
            update_status(mppt_info)
            return
    print("❌ No SmartSolar MPPT found.")

if __name__ == "__main__":
    asyncio.run(read_mppt())

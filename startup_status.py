import os
import time
import json
import socket
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from waveshare_epd import epd5in79

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "N/A"

def get_wifi_ssid():
    try:
        ssid = subprocess.check_output(["iwgetid", "-r"]).decode().strip()
        return ssid if ssid else "N/A"
    except:
        return "N/A"

def check_database():
    try:
        import sqlite3
        conn = sqlite3.connect("eink_data.db")
        conn.close()
        return True
    except:
        return False

def read_status_file():
    try:
        with open("status.json", "r") as f:
            return json.load(f)
    except:
        return {}

def render_status():
    # Init e-paper
    epd = epd5in79.EPD()
    epd.init()
    epd.Clear()

    WIDTH, HEIGHT = epd.width, epd.height
    image = Image.new("L", (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = get_ip_address()
    ssid = get_wifi_ssid()
    db_ok = check_database()

    # Start MPPT and BMS readers
    subprocess.Popen(["python3", "mppt_reader.py"])
    subprocess.Popen(["node", "bms_reader_debug.js"])

    # Wait for both to finish writing to status.json
    time.sleep(4)
    status = read_status_file()

    # Read MPPT
    mppt = status.get("mppt", {})
    mppt_name = mppt.get("name", "Not found")
    mppt_time = mppt.get("timestamp", "-")

    # Read BMS cell data
    cells = status.get("bms", {}).get("cells", {})

    draw.text((10, 10), f"{now}", font=font, fill=0)
    draw.text((10, 25), f"WiFi: {ssid}", font=font, fill=0)
    draw.text((10, 40), f"IP: {ip}", font=font, fill=0)
    draw.text((10, 55), f"DB: {'OK' if db_ok else 'ERROR'}", font=font, fill=0)

    draw.text((10, 75), f"MPPT: {mppt_name}", font=font, fill=0)
    draw.text((10, 90), f"Last: {mppt_time}", font=font, fill=0)

    # List BMS cell voltages
    y = 110
    for cell, v in sorted(cells.items()):
        draw.text((10, y), f"{cell}: {v:.3f}V", font=font, fill=0)
        y += 12
        if y > HEIGHT - 15:
            break  # avoid overflow

    epd.display(epd.getbuffer(image))
    time.sleep(5)
    epd.sleep()

if __name__ == "__main__":
    render_status()

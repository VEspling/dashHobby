import os
import subprocess
import socket
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import sqlite3
from waveshare_epd_py import epd5in79

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "N/A"

def get_ssid():
    try:
        result = subprocess.check_output(["iwgetid", "-r"]).decode().strip()
        return result if result else "N/A"
    except:
        return "N/A"

def run_external_scripts():
    os.system("python3 mppt_reader.py &")
    os.system("node bms_reader_debug.js &")

def load_status():
    try:
        import json
        with open("status.json", "r") as f:
            return json.load(f)
    except:
        return {}

def display_error(epd, message):
    WIDTH, HEIGHT = epd.width, epd.height
    image = Image.new("L", (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((10, 10), f"ERROR: {message}", font=font, fill=0)
    epd.display(epd.getbuffer(image))
    time.sleep(5)
    epd.sleep()

def main():
    try:
        epd = epd5in79.EPD()
        epd.init()
        epd.Clear()

        WIDTH, HEIGHT = epd.width, epd.height
        image = Image.new("L", (WIDTH, HEIGHT), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = get_ip_address()
        ssid = get_ssid()

        draw.text((10, 10), f"Time: {now}", font=font, fill=0)
        draw.text((10, 30), f"WiFi: {ssid}", font=font, fill=0)
        draw.text((10, 50), f"IP: {ip}", font=font, fill=0)

        try:
            conn = sqlite3.connect("eink_data.db")
            conn.close()
            draw.text((10, 70), "DB: OK", font=font, fill=0)
        except:
            draw.text((10, 70), "DB: ERROR", font=font, fill=0)

        status = load_status()
        bms_status = status.get("bms", "N/A")
        mppt_status = status.get("mppt", "N/A")

        draw.text((10, 90), f"BMS: {bms_status}", font=font, fill=0)
        draw.text((10, 110), f"MPPT: {mppt_status}", font=font, fill=0)

        epd.display(epd.getbuffer(image))
        time.sleep(5)
        epd.sleep()

        run_external_scripts()

    except Exception as e:
        try:
            epd = epd5in79.EPD()
            epd.init()
            display_error(epd, str(e))
        except:
            print(f"Startup failed: {e}")

if __name__ == "__main__":
    main()

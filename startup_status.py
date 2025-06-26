import time
import socket
import json
import os
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

def load_status():
    try:
        with open("status.json", "r") as f:
            return json.load(f)
    except:
        return {}

def render_status():
    epd = epd5in79.EPD()
    epd.init()
    epd.Clear()

    WIDTH, HEIGHT = epd.width, epd.height
    image = Image.new("L", (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = get_ip_address()
    status = load_status()

    draw.text((10, 10), f"Time: {now}", font=font, fill=0)
    draw.text((10, 30), f"IP: {ip}", font=font, fill=0)
    draw.text((10, 50), f"DB: {status.get('db', '...')}", font=font, fill=0)
    draw.text((10, 70), f"BMS: {status.get('bms', '...')}", font=font, fill=0)
    draw.text((10, 90), f"MPPT: {status.get('mppt', '...')}", font=font, fill=0)

    epd.display(epd.getbuffer(image))
    time.sleep(2)
    epd.sleep()

if __name__ == "__main__":
    while True:
        render_status()
        time.sleep(30)

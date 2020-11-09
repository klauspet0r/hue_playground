import time

import Adafruit_SSD1306
import sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess


def show_on_oled(*lines):
    disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)

    disp.begin()
    disp.clear()
    disp.display()

    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    padding = -2
    top = padding
    bottom = height - padding
    x = 0
    font_size = sys.argv[1]
    font = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf', font_size)

    #while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    # cmd = "ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'"
    # IP = subprocess.check_output(cmd, shell=True)
    # cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    # CPU = subprocess.check_output(cmd, shell = True )
    # cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    # MemUsage = subprocess.check_output(cmd, shell = True )
    # cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    # Disk = subprocess.check_output(cmd, shell = True )

    draw.text((x, top + font_size * 0), lines[0], font=font, fill=255)
    draw.text((x, top + font_size * 1), lines[1], font=font, fill=255)
    draw.text((x, top + font_size * 2), lines[2], font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(3)


line1 = 'HUE HUB'

cmd = "ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'"
line2 = subprocess.check_output(cmd, shell=True)
line2 = str(line2, 'utf-8')

line3 = '*   KLS1   *'

show_on_oled(line1, line2, line3)

#time.sleep(3)

show_on_oled(line1, line2, 'something else')

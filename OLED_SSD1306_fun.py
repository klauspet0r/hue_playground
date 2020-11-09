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

    padding = 1
    top = padding
    bottom = height - padding
    x = int(sys.argv[2])
    font_size = int(sys.argv[1])
    font = ImageFont.load_default()
    #font = ImageFont.truetype('8-bit-pusab.ttf', font_size)

    #while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width-1, height-1), outline=254, fill=0)

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
    time.sleep(1)


line1 = 'HUE HUB'

cmd = "ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'"
line2 = subprocess.check_output(cmd, shell=True)
line2 = str(line2, 'utf-8')

line3 = '*   KLS1   *'

try:

    while True:
        show_on_oled(line1, line2, line3)
        show_on_oled(line1, line2, 'something else')

except KeyboardInterrupt:
    print('Programm interrupted by Strg+C')

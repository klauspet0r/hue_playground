import argparse

from time import sleep

import Adafruit_SSD1306
import RPi.GPIO as GPIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

display = Adafruit_SSD1306.SSD1306_128_32(rst=None)

parser = argparse.ArgumentParser()
parser.add_argument('--ssd', type=float, default=0.1, help='this determines the scroll speed of the display')
parser.add_argument('--pts', type=float, default=1, help='this determines how many pixel are scrolled each time')
myargs = parser.parse_args()


def show_on_oled(lines, disp):
    disp.begin()
    disp.clear()
    disp.display()

    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    y = 0
    x = 0
    font_size = 8

    font = ImageFont.truetype('Minecraftia-Regular.ttf', font_size)

    # while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    line_counter = 0
    total_height = 0

    total_height = (font_size + 1) * len(lines)
    print('Total height of lines to be printed is: {} pixels'.format(total_height))

    direction = 1  # 1 is up,  -1 is down

    for y_dash in range(total_height):
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        for index, line in enumerate(lines):
            if y_dash <= total_height:
                draw.text((x, (y - y_dash * 2) + font_size * line_counter), lines[index], font=font, fill=255)
                line_counter += 1
                # TODO: Implement this in a way, that only the lines that fit the display are added to the image

        # elif total_height > max_display_height:

        line_counter = 1
        # Display image.
        disp.image(image)
        disp.display()
        sleep(myargs.ssd)


itemlist = ['Wohnzimmer', 'Küche', 'Schlafzimmer', 'Flur', 'pc', 'Spielecke', 'Küche Spots', 'tv', 'Esstisch',
            'Schreibtisch']

try:

    show_on_oled(itemlist, disp=display)

    #while True:
        #sleep(1)

except KeyboardInterrupt:  # Ctrl-C to terminate the program
    GPIO.cleanup()

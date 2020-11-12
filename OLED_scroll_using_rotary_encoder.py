import argparse

from time import sleep
from typing import Any, Union

import Adafruit_SSD1306
import RPi.GPIO as GPIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from InterfacePanel import InterfacePanel

rotary_encoder = (22, 27)

buttons = {"ok": 17}  # TODO: add button
# "back" : 19,
# "pause" : 5,
# "forward" : 16,
# "meny" : 12,


display = Adafruit_SSD1306.SSD1306_128_32(rst=None)

parser = argparse.ArgumentParser()
parser.add_argument('--ssd', type=float, default=0.1, help='this determines the scroll speed of the display')
parser.add_argument('--fs', type=int, default=13, help='this determines the font size in pixels')
parser.add_argument('--list', type=list, nargs='+', default=['Wohnzimmer',
                                                             'Küche',
                                                             'Schlafzimmer',
                                                             'Flur',
                                                             'Schreibtisch',
                                                             'Spielecke'], help='sets the list to be scrolled')
myargs = parser.parse_args()


def get_scroll_range(scroll_height):
    scroll_range = []

    for i in range(1, scroll_height - 4 + 1):
        scroll_range.append(i)

    for j in range(scroll_height - 3, 1, -1):
        scroll_range.append(j)

    return scroll_range


def show_on_oled(lines, position, disp):
    disp.begin()
    # disp.clear()
    disp.display()

    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    y_0 = 0
    x_0 = 0
    y_act = 0

    font_size = myargs.fs

    font = ImageFont.truetype('C&C Red Alert [INET].ttf', font_size)

    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    line_counter = 0

    total_height = (font_size + 1) * len(lines)

    scroll_height = total_height - height

    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    if -scroll_height <= y_act <= 0:

        y_act = y_0 - position

        for index, line in enumerate(lines):
            draw.text((x_0, y_act + (font_size * line_counter)), lines[index], font=font, fill=255)
            line_counter += 1
            # TODO: Implement this in a way, that only the lines that fit the display are added to the image
        line_counter = 0
        global y_act_nm1
        y_act_nm1 = y_act


    elif not (-scroll_height <= y_act <= 0):
        for index, line in enumerate(lines):
            draw.text((x_0, y_act_nm1 + (font_size * line_counter)), lines[index], font=font, fill=255)
            line_counter += 1
            # TODO: Implement this in a way, that only the lines that fit the display are added to the image

    disp.image(image)
    disp.display()
    sleep(myargs.ssd)


def rotation_callback(position, direction):
    show_on_oled(myargs.list, int((position / 4) - (position % 4)), display)


def button_callback(name):
    a = 1
    # if name in ["back", "forward"]:
    #     print("Button '{}' down....".format(name))
    #     return button_up
    # else:
    #     print("Button '{}' pressed.".format(name))
    #     return None


panel = InterfacePanel()

panel.add_rotary_encoder("Wheel", rotation_callback, *rotary_encoder)
for name, pin in buttons.items():
    panel.add_button(name, button_callback, pin)

# itemlist = ['Wohnzimmer', 'Küche', 'Schlafzimmer', 'Flur', 'Schreibtisch', 'Spielecke']

try:

    show_on_oled(myargs.list, disp=display)
    sleep(60)

except KeyboardInterrupt:  # Ctrl-C to terminate the program
    display.clear()

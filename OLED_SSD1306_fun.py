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
# parser.add_argument('--pts', type=float, default=1, help='this determines how many pixel are scrolled each time')
myargs = parser.parse_args()


def show_on_oled(lines, disp):
    disp.begin()
    disp.clear()
    disp.display()

    width = disp.width
    height = disp.height
    print('display height is: {}'.format(height))
    image = Image.new('1', (width, height))

    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    y_0 = 0
    x_0 = 0
    y_act = 0

    font_size = 8

    font = ImageFont.truetype('Minecraftia-Regular.ttf', font_size)

    # while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    line_counter = 0

    total_height = (font_size + 1) * len(lines)
    print('Total height of lines to be printed is: {} pixels'.format(total_height))

    direction = 1  # 0 is up for the first time, 1 is up,  -1 is down

    while True:
        scroll_height = total_height - height
        print('scroll_height = {}'.format(scroll_height))

        scroll_range_a = []
        scroll_range_b = []

        for i in range(0, scroll_height + 1):
            scroll_range_a.append(i)

        print('scroll_range_a is: {}'.format(scroll_range_a))

        for j in range(scroll_height, 1):
            scroll_range_b.append(-j)

        print('scroll_range_b is: {}'.format(scroll_range_b))

        scroll_range = scroll_range_a + scroll_range_b

        # for i in range(scroll_height, 1):
        #     scroll_range.append(-i)

        print('scroll_range is: {}'.format(scroll_range))

        for outer_index, y_dash in enumerate(scroll_range):
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            y_act = y_0 - y_dash
            print('y_act is: {}'.format(y_act))

            for inner_index, line in enumerate(lines):
                draw.text((x_0, y_act + font_size * line_counter), lines[inner_index], font=font, fill=255)
                line_counter += 1
                # TODO: Implement this in a way, that only the lines that fit the display are added to the image

            # elif total_height > max_display_height:

            line_counter = 1
            # Display image.
            disp.image(image)
            disp.display()
            sleep(myargs.ssd)

    # if direction == -1:
    #     for y_dash in range(0, total_height + height):
    #         draw.rectangle((0, 0, width, height), outline=0, fill=0)
    #         y_act = -total_height + y_dash + 1
    #
    #         for index, line in enumerate(lines):
    #
    #             draw.text((x_0, y_act + font_size * line_counter), lines[index], font=font, fill=255)
    #             line_counter += 1
    #             # TODO: Implement this in a way, that only the lines that fit the display are added to the image
    #
    #         # elif total_height > max_display_height:
    #
    #         line_counter = 1
    #         # Display image.
    #         disp.image(image)
    #         disp.display()
    #         sleep(myargs.ssd)
    #
    #         if y_act >= height:
    #             direction = -1


itemlist = ['Wohnzimmer', 'Küche', 'Schlafzimmer', 'Flur', 'Schreibtisch']

try:

    show_on_oled(itemlist, disp=display)

except KeyboardInterrupt:  # Ctrl-C to terminate the program
    GPIO.cleanup()

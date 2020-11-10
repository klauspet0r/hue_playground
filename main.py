from RotaryEncoder import RotaryEncoder

from time import sleep
import sys
import os

import Adafruit_SSD1306
import RPi.GPIO as GPIO
import phue
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

display = Adafruit_SSD1306.SSD1306_128_32(rst=None)


def show_on_oled(lines, disp):
    disp.begin()
    disp.clear()
    disp.display()

    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    padding = 0
    y = padding
    bottom = height - padding
    x = 0
    font_size = 8
    # font = ImageFont.load_default()
    font = ImageFont.truetype('Minecraftia-Regular.ttf', font_size)

    # while True:
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

    line_counter = 0
    total_height = 0
    max_display_height = 32

    total_height = (font_size + 1) * len(lines)

    for y_dash in range(total_height):
        disp.clear()
        disp.display()

        for index, line in enumerate(lines):
            # max_width, max_height = draw.textsize(line, font=font)
            print(str(total_height))
            draw.text((x, (y - y_dash) + font_size * line_counter), lines[index], font=font, fill=255)
            line_counter += 1
        # elif total_height > max_display_height:

        line_counter = 1
        # Display image.
        disp.image(image)
        disp.display()
        sleep(1)


# import extract_dicts_from_api

clk = 22  # gpio pin for clk
dt = 23  # gpio pin for dt
sw = 24  # gpio pin for the button
list_index = 0
itemlist = []

# def cls():
#     os.system('cls' if os.name == 'nt' else 'clear')


# def print_item(itemlist):
#     #cls()
#     print('\n')
#     print('++++++++++++++++++++++++++++++++++++++++++++')
#     print('*')
#     print('*')
#     print('*        #' + str(list_index + 1) + ' Group: ' + itemlist[list_index] + '')
#     print('*')
#     print('*')
#     print('++++++++++++++++++++++++++++++++++++++++++++')


# def decode_rotation(clk):
#     global list_index
#
#     sleep(0.02)  # extra 2 mSec de-bounce time
#     # read both of the switches
#     CLK = GPIO.input(clk)
#     DT = GPIO.input(dt)
#
#     sleep(0.002)  # extra 2 mSec de-bounce time
#
#     if (CLK == 1) and (DT == 0):
#         list_index += 1
#         if list_index > len(itemlist) - 1:
#             list_index = 0
#         print_item(itemlist)
#
#         while DT == 0:
#             DT = GPIO.input(dt)
#         # now wait for B to drop to end the click cycle
#         while DT == 1:
#             DT = GPIO.input(dt)
#         return
#
#     elif (CLK == 1) and (DT == 1):
#         list_index -= 1
#         if list_index < 0 or list_index > len(itemlist):
#             list_index = len(itemlist) - 1
#         print_item(itemlist)
#         while CLK == 1:
#             CLK = GPIO.input(clk)
#         return
#
#     else:  # discard all other combinations
#         return


# def button_callback(sw):
#     print('!buttonpushed!')
#     global itemlist
#     global list_index
#     itemlist = groups[itemlist[list_index]]
#     list_index = 0
#     print('before print_item(itemlist)')
#     print_item(itemlist)
#     print('after print_item(itemlist)')


try:

    bridge_ip = '192.168.2.100'

    bridge = phue.Bridge(str(bridge_ip))

    bridge.connect()

    api_response = bridge.get_api()

    messages = ["Connected to Brigde", "No. of lamps: " + str(len(api_response['lights'])),
                'Number of groups: ' + str(len(api_response['groups']))]

    show_on_oled(messages, disp=display)

    lights = {}
    groups = {}


    def fill_lights_dict():
        global lights
        for key, value in api_response['lights'].items():
            lights[key] = value['name']


    def fill_groups_dict():
        global groups
        for key, value in api_response['groups'].items():
            groups[value['name']] = value['lights']


    def correlate_names_to_numbers():
        for key, value in groups.items():
            for i in range(len(value)):
                value[i] = lights[value[i]]


    fill_lights_dict()
    fill_groups_dict()
    correlate_names_to_numbers()

    # print(str(api_response['lights'].items()))

    for key, value in groups.items():
        itemlist.append(key)

    # rotary_encoder = RotaryEncoder(clk, dt, sw, decode_rotation, button_callback)

    show_on_oled(itemlist, disp=display)

    while True:
        sleep(1)

except KeyboardInterrupt:  # Ctrl-C to terminate the program
    GPIO.cleanup()

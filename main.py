from RotaryEncoder import RotaryEncoder

from time import sleep
import sys
import os

import RPi.GPIO as GPIO
import phue

import extract_dicts_from_api

clk = 22  # gpio pin for clk
dt = 23  # gpio pin for dt
sw = 24  # gpio pin for the button
list_index = 0
itemlist = []


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_item(itemlist):
    #cls()
    print('\n')
    print('++++++++++++++++++++++++++++++++++++++++++++')
    print('*')
    print('*')
    print('*        #' + str(list_index + 1) + ' Group: ' + itemlist[list_index] + '')
    print('*')
    print('*')
    print('++++++++++++++++++++++++++++++++++++++++++++')


def decode_rotation(clk):
    global list_index

    sleep(0.02)  # extra 2 mSec de-bounce time
    # read both of the switches
    CLK = GPIO.input(clk)
    DT = GPIO.input(dt)

    sleep(0.002)  # extra 2 mSec de-bounce time

    if (CLK == 1) and (DT == 0):
        list_index += 1
        if list_index > len(itemlist) - 1:
            list_index = 0
        print_item(itemlist)

        while DT == 0:
            DT = GPIO.input(dt)
        # now wait for B to drop to end the click cycle
        while DT == 1:
            DT = GPIO.input(dt)
        return

    elif (CLK == 1) and (DT == 1):
        list_index -= 1
        if list_index < 0 or list_index > len(itemlist):
            list_index = len(itemlist) - 1
        print_item(itemlist)
        while CLK == 1:
            CLK = GPIO.input(clk)
        return

    else:  # discard all other combinations
        return


def button_callback(sw):
    print('!buttonpushed!')
    global itemlist
    global list_index
    itemlist = groups[itemlist[list_index]]
    list_index = 0
    print('before print_item(itemlist)')
    print_item(itemlist)
    print('after print_item(itemlist)')




try:

    bridge_ip = str(sys.argv[1])

    bridge = phue.Bridge(str(bridge_ip))

    bridge.connect()

    api_response = bridge.get_api()
    print('\nConnected to bridge @ IP ' + str(bridge_ip) + '\n')
    print('Number of connected lamps: ' + str(len(api_response['lights'])) + '\n')
    print('Number of groups: ' + str(len(api_response['groups'])) + '\n')

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

    rotary_encoder = RotaryEncoder(clk, dt, sw, decode_rotation, button_callback)

    while True:
        sleep(1)

except KeyboardInterrupt:  # Ctrl-C to terminate the program
    GPIO.cleanup()

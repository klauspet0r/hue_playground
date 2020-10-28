# -*- coding: iso-8859-1 -*-
from RotaryEncoder import RotaryEncoder

from time import sleep
import sys

import RPi.GPIO as GPIO
import phue

clk = 22  # gpio pin for clk
dt = 23  # gpio pin for dt
decoder_counter = 0
lamplist = []


def decode_rotation(clk):
    sleep(0.002)  # debounce time

    global decoder_counter

    CLK = GPIO.input(clk)
    DT = GPIO.input(dt)

    sleep(0.002)  # extra 2 mSec de-bounce time

    if (CLK == 1) and (DT == 0):
        decoder_counter += 1
        print(str(decoder_counter))
        while DT == 0:
            DT = GPIO.input(dt)

        while DT == 1:
            DT = GPIO.input(dt)
        value_changed = True
        return

    elif (CLK == 1) and (DT == 1):
        decoder_counter -= 1
        print(str(decoder_counter))
        while CLK == 1:
            CLK = GPIO.input(clk)
        value_changed = True
        return

    else:  # discard all other combinations
        value_changed = False
        return


try:

    bridge_ip = str(sys.argv[1])

    bridge = phue.Bridge(str(bridge_ip))

    bridge.connect()

    api_response = bridge.get_api()
    print('\nConnected to bridge @ IP ' + str(bridge_ip) + '\n')
    print('Number of connected Lamps: ' + str(len(api_response['lights'])) + '\n')

    #print(str(api_response['lights'].items()))

    for key, value in api_response['lights'].items():
        print(str(value['name']).decode("iso-8859-1").encode("iso-8859-1") + '\n')
        lamplist.append(value['name'])


    print(lamplist)

    rotary_encoder = RotaryEncoder(clk, dt, decode_rotation)

    while True:
        sleep(1)

except KeyboardInterrupt:  # Ctrl-C to terminate the program
    GPIO.cleanup()

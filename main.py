from RotaryEncoder import RotaryEncoder
from time import sleep
import RPi.GPIO as GPIO

clk = 22
dt = 23
decoder_counter = 0

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

    rotary_encoder = RotaryEncoder(clk, dt, decode_rotation)

    while True:
        sleep(0.01)

except KeyboardInterrupt:  # Ctrl-C to terminate the program
    GPIO.cleanup()

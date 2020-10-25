import RPi.GPIO as GPIO
from time import sleep

# GPIO Ports
clk = 22  # Encoder input A: input GPIO 23 (active high)
dt = 23  # Encoder input B: input GPIO 24 (active high)


# gpio_list = [clk, dt]


def init_rotary_decoder():
    GPIO.setwarnings(True)

    # Use the Raspberry Pi BCM pins
    GPIO.setmode(GPIO.BCM)

    # define the Encoder switch inputs
    GPIO.setup(clk, GPIO.IN)  # pull-ups are too weak, they introduce noise
    GPIO.setup(dt, GPIO.IN)

    # setup an event detection thread for the A encoder switch
    GPIO.add_event_detect(clk, GPIO.RISING, callback=decode_rotation, bouncetime=2)  # bouncetime in mSec

    return


def decode_rotation(clk):
    # read both of the switches
    CLK = GPIO.input(clk)
    DT = GPIO.input(dt)

    sleep(0.002)  # extra 2 mSec de-bounce time

    if (CLK == 1) and (DT == 0):
        print("clockwise")
        while DT == 0:
            DT = GPIO.input(dt)
        # now wait for B to drop to end the click cycle
        while DT == 1:
            DT = GPIO.input(dt)
        return

    elif (CLK == 1) and (DT == 1):
        print("counterclockwise")
        # A is already high, wait for A to drop to end the click cycle
        while CLK == 1:
            CLK = GPIO.input(clk)
        return

    else:  # discard all other combinations
        return


try:
    init_rotary_decoder()
    while True:
        sleep(1)

except KeyboardInterrupt:  # Ctrl-C to terminate the program
    GPIO.cleanup()

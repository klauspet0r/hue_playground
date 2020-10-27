import RPi.GPIO as GPIO
from time import sleep


class RotaryEncoder:
    decoder_counter = None
    value_changed = None
    clk = None
    dt = None

    def __init__(self, clk, dt, decode_rotation):

        self.value_changed = False
        self.decoder_counter = 0
        self.clk = clk
        self.dt = dt

        GPIO.setwarnings(True)

        # Use the Raspberry Pi BCM pins
        GPIO.setmode(GPIO.BCM)

        # define the Encoder switch inputs
        GPIO.setup(clk, GPIO.IN)  # pull-ups are too weak, they introduce noise
        GPIO.setup(dt, GPIO.IN)

        # setup an event detection thread for the A encoder switch
        GPIO.add_event_detect(clk, GPIO.RISING, callback=decode_rotation, bouncetime=2)  # bouncetime in mSec

        return

    def get_value_change(self):
        return self.value_changed

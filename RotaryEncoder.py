import RPi.GPIO as GPIO
from time import sleep


class RotaryEncoder:
    decoder_counter = None
    value_changed = None
    clk = None
    dt = None

    def __init__(self, clk, dt, sw, decode_rotation, button_callback):
        self.decoder_counter = 0
        self.clk = clk
        self.dt = dt
        self.sw = sw

        GPIO.setwarnings(True)

        # Use the Raspberry Pi BCM pins
        GPIO.setmode(GPIO.BCM)

        # define the Encoder switch inputs
        GPIO.setup(clk, GPIO.IN)  # pull-ups are too weak, they introduce noise
        GPIO.setup(dt, GPIO.IN)
        GPIO.setup(sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # setup an event detection thread for the A encoder switch
        GPIO.add_event_detect(clk, GPIO.RISING, callback=decode_rotation, bouncetime=20)  # bouncetime in mSec
        GPIO.add_event_detect(sw, GPIO.RISING, callback=button_callback)

        return


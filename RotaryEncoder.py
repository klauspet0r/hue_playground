import RPi.GPIO as GPIO
from time import sleep

class RotaryEncoder:

    decoder_counter = 1

    def __init__(self, clk, dt):

        GPIO.setwarnings(True)

        # Use the Raspberry Pi BCM pins
        GPIO.setmode(GPIO.BCM)

        # define the Encoder switch inputs
        GPIO.setup(clk, GPIO.IN)  # pull-ups are too weak, they introduce noise
        GPIO.setup(dt, GPIO.IN)

        # setup an event detection thread for the A encoder switch
        GPIO.add_event_detect(clk, GPIO.RISING, callback=self.decode_rotation, bouncetime=2)  # bouncetime in mSec

        return

    def decode_rotation(clk, dt, decoder_counter):

        sleep(0.002)  # debounce time

        CLK = GPIO.input(clk)
        DT = GPIO.input(dt)

        sleep(0.002)  # extra 2 mSec de-bounce time

        if (CLK == 1) and (DT == 0):
            decoder_counter += 1
            while DT == 0:
                DT = GPIO.input(dt)
            # now wait for B to drop to end the click cycle
            while DT == 1:
                DT = GPIO.input(dt)
            return

        elif (CLK == 1) and (DT == 1):
            decoder_counter -= 1
            while CLK == 1:
                CLK = GPIO.input(clk)
            return

        else:  # discard all other combinations
            return


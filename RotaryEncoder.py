import RPi.GPIO as GPIO
from time import sleep


class RotaryEncoder:
    decoder_counter = None
    value_changed = None
    clk = None
    dt = None

    def __init__(self, clk, dt):

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
        GPIO.add_event_detect(clk, GPIO.RISING, callback=self.decode_rotation, bouncetime=2)  # bouncetime in mSec

        return

    def decode_rotation(self, clk):

        sleep(0.002)  # debounce time

        CLK = GPIO.input(self.clk)
        DT = GPIO.input(self.dt)

        sleep(0.002)  # extra 2 mSec de-bounce time

        if (CLK == 1) and (DT == 0):
            print(str('self.decoder_counter += 1'))
            self.decoder_counter += 1
            while DT == 0:
                DT = GPIO.input(self.dt)

            while DT == 1:
                DT = GPIO.input(self.dt)
            value_changed = True
            return

        elif (CLK == 1) and (DT == 1):
            print(str('self.decoder_counter -= 1'))
            self.decoder_counter -= 1
            while CLK == 1:
                CLK = GPIO.input(self.clk)
            value_changed = True
            return

        else:  # discard all other combinations
            value_changed = False
            return

    def get_value_change(self):
        return self.value_changed

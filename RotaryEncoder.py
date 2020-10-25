import RPi.GPIO as GPIO
from time import sleep

class RotaryEncoder:

    def __init__(self, clk_pin, dt_pin):
        self.clk_pin = clk_pin
        self.dt_pin = dt_pin
        #self.button_pin = button_pin #TODO: add a button to this class
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(clk_pin, GPIO.IN)  # pull-ups are too weak, they introduce noise
        GPIO.setup(dt_pin, GPIO.IN)
        # setup an event detection thread for the A encoder switch
        GPIO.add_event_detect(clk_pin, GPIO.RISING, callback=self.decode_rotation, bouncetime=2)

    def decode_rotation(self):
        global counter
        sleep(0.002) #additional debounce time
        # read both of the switches
        Switch_A = GPIO.input(self.clk_pin)
        Switch_B = GPIO.input(self.dt_pin)

        if (Switch_A == 1) and (Switch_B == 0):  # A then B ->
            counter += 1
            direction = 1
            print(direction, counter)
            # at this point, B may still need to go high, wait for it
            while Switch_B == 0:
                Switch_B = GPIO.input(self.dt_pin)
            # now wait for B to drop to end the click cycle
            while Switch_B == 1:
                Switch_B = GPIO.input(self.dt_pin)
            return

        elif (Switch_A == 1) and (Switch_B == 1):  # B then A <-
            counter -= 1
            direction = -1
            print(direction, counter)
            # A is already high, wait for A to drop to end the click cycle
            while Switch_A == 1:
                Switch_A = GPIO.input(self.clk_pin)
            return

        else:  # discard all other combinations
            return


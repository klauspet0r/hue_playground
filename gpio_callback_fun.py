import RPi.GPIO as GPIO
from time import sleep


def rotation_decode(Enc_A):

    # read both of the switches
    Switch_A = GPIO.input(Enc_A)
    Switch_B = GPIO.input(Enc_B)

    if (Switch_A == 1) and (Switch_B == 0):
        print("clockwise")
        while Switch_B == 0:
            Switch_B = GPIO.input(Enc_B)
        # now wait for B to drop to end the click cycle
        while Switch_B == 1:
            Switch_B = GPIO.input(Enc_B)
        return

    elif (Switch_A == 1) and (Switch_B == 1):
        print("counterclockwise")
        # A is already high, wait for A to drop to end the click cycle
        while Switch_A == 1:
            Switch_A = GPIO.input(Enc_A)
        return
    
    else: # discard all other combinations
        return

counter = 0

# GPIO Ports
Enc_A = 23  # Encoder input A: input GPIO 23 (active high)
Enc_B = 24  # Encoder input B: input GPIO 24 (active high)

GPIO.setwarnings(True)

# Use the Raspberry Pi BCM pins
GPIO.setmode(GPIO.BCM)

# define the Encoder switch inputs
GPIO.setup(Enc_A, GPIO.IN) # pull-ups are too weak, they introduce noise
GPIO.setup(Enc_B, GPIO.IN)

# setup an event detection thread for the A encoder switch
GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotation_decode, bouncetime=2) # bouncetime in mSec

while(True):

    try:
        sleep(1)

    except KeyboardInterrupt: # Ctrl-C to terminate the program
        GPIO.cleanup()


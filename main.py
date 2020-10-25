from RotaryEncoder import RotaryEncoder
from time import sleep
import RPi.GPIO as GPIO

try:

    rotary_encoder = RotaryEncoder(22, 23)

    while True:

        while rotary_encoder.get_value_change():
            print(str(rotary_encoder.decoder_counter))
            sleep(1)

except KeyboardInterrupt:  # Ctrl-C to terminate the program
    GPIO.cleanup()

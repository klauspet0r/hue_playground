import RotaryEncoder
from RotaryEncoder import RotaryEncoder

rotary_encoder = RotaryEncoder(22, 23)

while True:
    print(str(rotary_encoder.decoder_counter))



try:
    rotary_encoder = RotaryEncoder(22, 23)

    while True:
        sleep(2)

except KeyboardInterrupt:  # Ctrl-C to terminate the program
    GPIO.cleanup()
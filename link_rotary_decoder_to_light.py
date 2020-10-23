import phue
import sys
from gpiozero import Button
import RPi.GPIO as GPIO
import threading
from time import sleep

button = Button(24)  # TODO:

bridge = phue.Bridge(str(sys.argv[1]))

bridge.connect()

api_response = bridge.get_api()

print('Press button to get Lampnames\n')

while True:

    if button.is_pressed:
        print('Number of connected Lamps: ' + str(len(api_response['lights'])) + '\n')

        print('All lamp names: \n')
        print('+++++++++++++++ \n')
        for key, value in api_response['lights'].items():
            print("#" + key + ' ' + value['name'])
            # for entry in api_response['lights'][key].items():
            # print(entry['name'])
        break

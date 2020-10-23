import phue
import sys
from gpiozero import Button
#import RPi.GPIO as GPIO
#import threading
from time import sleep
from consolemenu import *
from consolemenu.items import *

button = Button(24)  # TODO:

bridge_ip = str(sys.argv[1])

bridge = phue.Bridge(str(bridge_ip))

menu = ConsoleMenu("Lamps", "")

while True:

    print('Push Button to connect to bridge @ IP:' + str(bridge_ip) + '\n')
    button.wait_for_press()

    if button.is_pressed:
        bridge.connect()

        api_response = bridge.get_api()
        print('Connected to bridge @ IP ' + str(bridge_ip) + '\n')
        print('Number of connected Lamps: ' + str(len(api_response['lights'])) + '\n')
        break

print('\n Press button to get Lampnames\n')


lamplist =[]

for key,values in api_response['lights'].items():

    lamplist.append(key)

selection_menu = SelectionMenu(lamplist)

menu.append_item(selection_menu)
menu.show()


# while True:
#
#     if button.is_pressed:
#
#         print('All lamp names: \n')
#         print('+++++++++++++++ \n')
#         for key, value in api_response['lights'].items():
#             print("#" + key + ' ' + value['name'])
#             # for entry in api_response['lights'][key].items():
#             # print(entry['name'])
#         break

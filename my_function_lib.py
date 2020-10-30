# decode_rotation hoch und runter zählen

# def decode_rotation(clk):
#     sleep(0.002)  # debounce time
#
#     global decoder_counter
#
#     CLK = GPIO.input(clk)
#     DT = GPIO.input(dt)
#
#     sleep(0.002)  # extra 2 mSec de-bounce time
#
#     if (CLK == 1) and (DT == 0):
#         decoder_counter += 1
#         print(str(decoder_counter))
#         while DT == 0:
#             DT = GPIO.input(dt)
#
#         while DT == 1:
#             DT = GPIO.input(dt)
#         value_changed = True
#         return
#
#     elif (CLK == 1) and (DT == 1):
#         decoder_counter -= 1
#         print(str(decoder_counter))
#         while CLK == 1:
#             CLK = GPIO.input(clk)
#         value_changed = True
#         return
#
#     else:  # discard all other combinations
#         value_changed = False
#         return


#decode_rotation list browsing

# def decode_rotation(clk):
#     global list_index
#
#     sleep(0.002)  # extra 2 mSec de-bounce time
#     # read both of the switches
#     CLK = GPIO.input(clk)
#     DT = GPIO.input(dt)
#
#     sleep(0.002)  # extra 2 mSec de-bounce time
#
#     if (CLK == 1) and (DT == 0):
#         list_index += 1
#         if list_index > len(list_of_rooms) - 1:
#             list_index = 0
#         cls()
#         print('\n')
#         print('********************************************')
#         print('#: ' + str(list_index + 1) + ' Raum: ' + list_of_rooms[list_index])
#         print('********************************************')
#         while DT == 0:
#             DT = GPIO.input(dt)
#         # now wait for B to drop to end the click cycle
#         while DT == 1:
#             DT = GPIO.input(dt)
#         return
#
#     elif (CLK == 1) and (DT == 1):
#         list_index -= 1
#         if list_index < 0 or list_index > len(list_of_rooms):
#             list_index = len(list_of_rooms) - 1
#         cls()
#         print('\n')
#         print('********************************************')
#         print('#: ' + str(list_index + 1) + ' Raum: ' + list_of_rooms[list_index])
#         print('********************************************')
#         while CLK == 1:
#             CLK = GPIO.input(clk)
#         return
#
#     else:  # discard all other combinations
#         return
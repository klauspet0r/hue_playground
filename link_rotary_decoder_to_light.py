import phue
import sys

bridge = phue.Bridge(str(sys.argv[1]))



bridge.connect()

api_response = bridge.get_api()

print('Number of connected Lamps: ' + str(len(api_response['lights'])) + '\n')

print('All lamp names: \n')
print('+++++++++++++++ \n')
for key, value in api_response['lights'].items():
    print("#" + key + ' ' + value['name'])
    #for entry in api_response['lights'][key].items():
        #print(entry['name'])








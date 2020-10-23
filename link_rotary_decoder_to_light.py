import phue
import sys

bridge = phue.Bridge(str(sys.argv[1]))



bridge.connect()

api_response = bridge.get_api()

print('length of api dictionary is: ' + str(len(api_response['lights'])))

print('All lamp names: \n')
for key, value in api_response['lights'].items():
    print("#" + key + ' Lampname: ' + value['name'])
    #for entry in api_response['lights'][key].items():
        #print(entry['name'])








import phue
import sys

bridge = phue.Bridge(str(sys.argv[1]))



bridge.connect()

api_response = bridge.get_api()

print('length of api dictionary is: ' + str(len(api_response)))

print('list of the keys in the api dict:  ' + str(api_response.keys()))

#print(api_response.keys().[1])

print('lights are: ' + str(api_response['lights'].keys()))





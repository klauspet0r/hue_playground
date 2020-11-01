import phue
import sys

bridge_ip = str(sys.argv[1])

bridge = phue.Bridge(str(bridge_ip))

bridge.connect()

api_response = bridge.get_api()

print('Connected to bridge @ IP ' + str(bridge_ip) + '\n')


lights = {}
groups = {}

for key, value in api_response['lights'].items():
    lights[key] = value['name']

print(str(lights).replace('\',', '\',\n'))
print('\n')

for key, value in api_response['groups'].items():
    groups[value['name']] = value['lights']


print(str(groups).replace('],', '],\n'))
print('\n')

for key, value in groups.items():
    for i in range(len(value)):
        value[i] = lights[value[i]]

print(str(groups).replace('],', '],\n'))




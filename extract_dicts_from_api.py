import phue
import sys

bridge = phue.Bridge(sys.argv[1])

bridge.connect()

print('\nConnected to bridge' + str(sys.argv[1]) + '\n')

api_response = bridge.get_api()

lights = {}
groups = {}


def fill_lights_dict():
    global lights
    for key, value in api_response['lights'].items():
        lights[key] = value['name']


def fill_groups_dict():
    global groups
    for key, value in api_response['groups'].items():
        groups[value['name']] = value['lights']


fill_lights_dict()
fill_groups_dict()

print(str(lights).replace('\',', '\',\n'))
print('\n')

print(str(groups).replace('],', '],\n'))
print('\n')


def correlate_names_to_numbers():
    for key, value in groups.items():
        for i in range(len(value)):
            value[i] = lights[value[i]]


correlate_names_to_numbers()

print(str(groups).replace('],', '],\n'))

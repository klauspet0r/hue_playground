import phue
import sys


def connect_to_bridge(bridge):
    bridge.connect()

    print('\nConnected to bridge \n')

    return bridge


def get_api_response(bridge):
    connect_to_bridge(bridge)
    return bridge.get_api()


bridge = phue.Bridge(str(sys.argv[0]))

api_response = get_api_response(bridge)

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

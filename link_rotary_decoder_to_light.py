import phue

bridge = phue.Bridge('192.168.2.100')


bridge.connect()

print(bridge.get_api())


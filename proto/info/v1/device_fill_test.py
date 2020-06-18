import info_pb2

device = info_pb2.Device()

# set device version
ver = device.version
ver.major = 1
ver.minor = 0
ver.micro = 1

device.unique_id = "5A:63:B4" # last 3 octets of MAC addr

device.hardware_id = 'Adafruit PyPortal with samd51j20'

device.bat_level = 3.4 # battery level, in Volts

loc = device.location

loc.lat = 38.1123
loc.lon = -91.2325
loc.ele = 112

print(device)

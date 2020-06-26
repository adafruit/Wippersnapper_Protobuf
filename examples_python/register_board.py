# Example for registering a device with
# the Adafruit IO BlinkaConnect server
import sys
sys.path.insert(1, 'registration/v1')

import registration_pb2

device = registration_pb2.Device()

# User-assigned device name (MQTT Client ID)
device.name = "PyPortal"
# PyPortal VID
device.vid = 0x239A
# PyPortal PID
device.pid = 0x8036

# Connection type
device.transport = device.TRANSPORT_WIFI

# TODO: All of the above should be kept in the library,
# or some type of master repository so one could
# pass the device name into blinkaconnect
# NOTE: The library should also contain the board's pin
# mapping in addition to capibilities of each pin in the map

# blinkaconnect library version
device.version.major = 0
device.version.minor = 0
device.version.micro = 1
device.version.label = "alpha.1"

print(device)
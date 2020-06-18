# Python generated code
import info_pb2

# CPython3 imports
import random
from uuid import getnode as get_mac

# BlinkaConnect library version
__version__ = "0.0.1-auto.0"

device = info_pb2.Device()

# device version based off FW version
ver = device.version
ver.major = int(__version__[0])
ver.minor = int(__version__[2])
ver.micro = int(__version__[4])

# UUID from last 3 octets of MAC
device.unique_id = hex(get_mac())[8:]

device_id = 'Adafruit PyPortal with samd51j20'
device.hardware_id = device_id

# battery level, in Volts
device.bat_level = random.uniform(0, 5)

# device location
loc = device.location
loc.lat = random.uniform(-90, 90)
loc.lon = random.uniform(-180, 180)
loc.ele = random.uniform(-20000, 20000)

# output the device model
print(device)

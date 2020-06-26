# Example for registering a device with
# the Adafruit IO BlinkaConnect server
import sys
sys.path.insert(1, 'registration/v1')

import registration_pb2

__version__ = "0.0.0-alpha.1"
PYPORTAL_VID = 0x239A
PYPORTAL_PID = 0x8036

device = registration_pb2.Device()

# User-assigned device name (MQTT Client ID)
device.display_name = "PyPortal"
# PyPortal VID
device.usb_vid = PYPORTAL_VID
# PyPortal PID
device.usb_pid = PYPORTAL_PID

# Connection type
device.transport = device.TRANSPORT_WIFI

# blinkaconnect code.py version
ver = __version__.split("-")
device.version.major = int(ver[0].split(".")[0])
device.version.minor = int(ver[0].split(".")[1])
device.version.micro = int(ver[0].split(".")[2])
device.version.label = ver[1]

print(device)
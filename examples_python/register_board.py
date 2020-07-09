# Example for registering a device with
# the Adafruit IO BlinkaConnect server
import sys
sys.path.insert(1, 'description/v1')

import description_pb2


# Request sent by device to Adafruit IO
# to set the board definition to a PyPortal
pyportal = description_pb2.CreateDescriptionRequest()

pyportal.display_name = "PyPortal"
pyportal.usb_vid = 0x239A
pyportal.usb_pid = 0x8036
pyportal.version.major = 0
pyportal.version.minor = 0
pyportal.version.micro = 0
pyportal.version.label = "alpha.1"

print(pyportal)

# Request sent by a device to Adafruit IO
# on `device/ID/description/get` to request the board
# definition as a string
definition = description_pb2.GetDefinitionRequest()
definition.data = "\0"

print(definition)
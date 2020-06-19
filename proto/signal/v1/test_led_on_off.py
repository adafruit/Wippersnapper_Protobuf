# This code sends messages across a
# signal to set up and turn on/off a LED
# from Adafruit IO to a device

import signal_pb2

def serialize_protobuf(buf):
    buf = buf.SerializeToString()
    print('Serialized Protobuf: ', buf)
    print('length: %i bytes'%len(buf))


signal = signal_pb2.Signal()

"""
led = digitalio.DigitalInOut(D13)
led.direction = digitalio.Direction.OUTPUT
"""
command = signal.cmd_pin
# command message
command.command.type = signal.CMD_TYPE_SET
command.command.name = signal.CMD_NAME_PIN_MODE
# pin message
command.pin = 13
command.mode = signal.cmd_pin.PIN_MODE_DIGITAL
command.direction = signal.cmd_pin.PIN_DIRECTION_OUTPUT

print(signal)
serialize_protobuf(signal)

signal.Clear() # Clear the command on the signal message

"""
led.Value = True
"""
command = signal.cmd_pin
# command message
command.command.type = signal.CMD_TYPE_SET
command.command.name = signal.CMD_NAME_PIN_VALUE
# pin message
command.pin = 13
command.command.value = "True"

print(signal)
serialize_protobuf(signal)
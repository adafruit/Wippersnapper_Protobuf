# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT

# Messages transmitted by Adafruit IO
# to toggle a LED on a device

import signal_pb2

def serialize_protobuf(buf):
    """Serializes protobuf
    to a string. Displays the protobuf and
    the protobuf information.

    """
    buf = buf.SerializeToString()
    print('Serialized Protobuf: ', buf)
    print('length: %i bytes'%len(buf))

# Create new signal message
signal = signal_pb2.Signal()

"""
PUBLISH from Adafruit IO to Device

Set up a digital pin as an output.
"""
command = signal.cmd
# command message
command.type = signal.CMD_TYPE_SET
command.name = signal.CMD_NAME_PIN_MODE
# pin message
command.pin_info.pin = "D13"
command.pin_info.mode = signal.pin_info.MODE_DIGITAL
command.pin_info.direction = signal.pin_info.DIRECTION_OUTPUT

print(signal)
serialize_protobuf(signal)
signal.Clear()

"""
PUBLISH from Adafruit IO to Device

Set the pin's digital logic level to True.
"""
command = signal.cmd
# command message
command.type = signal.CMD_TYPE_SET
command.name = signal.CMD_NAME_PIN_VALUE
# pin message
command.pin_info.pin = "D13"
command.pin_info.value = "True"

print(signal)
serialize_protobuf(signal)
signal.Clear()

"""
PUBLISH from Adafruit IO to Device

Set the pin's digital logic level to False.
"""
command = signal.cmd
# command message
command.type = signal.CMD_TYPE_SET
command.name = signal.CMD_NAME_PIN_VALUE
# pin message
command.pin_info.pin = "D13"
command.pin_info.value = "False"

print(signal)
serialize_protobuf(signal)
signal.Clear()

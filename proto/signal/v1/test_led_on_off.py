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
led = digitalio.DigitalInOut(D13)
led.direction = digitalio.Direction.OUTPUT
"""
cmd = signal.pin_cmd
# command message
cmd.command.type = signal.CMD_TYPE_SET
cmd.command.name = signal.CMD_NAME_PIN_MODE
# pin message
cmd.pin = 13
cmd.mode = signal.pin_cmd.MODE_DIGITAL
cmd.direction = signal.pin_cmd.DIRECTION_OUTPUT

print(signal)
serialize_protobuf(signal)
signal.Clear()

"""
led.Value = True
"""
cmd = signal.pin_cmd
# command message
cmd.command.type = signal.CMD_TYPE_SET
cmd.command.name = signal.CMD_NAME_PIN_VALUE
# pin message
cmd.pin = 13
cmd.command.value = "True"

print(signal)
serialize_protobuf(signal)
signal.Clear()

"""
led.Value = False
"""
cmd = signal.pin_cmd
# command message
cmd.command.type = signal.CMD_TYPE_SET
cmd.command.name = signal.CMD_NAME_PIN_VALUE
# pin message
cmd.pin = 13
cmd.command.value = "False"

print(signal)
serialize_protobuf(signal)
signal.Clear()

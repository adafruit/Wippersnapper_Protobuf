# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT

# strict system paths
import sys
sys.path.insert(1, 'semver/v1')
sys.path.insert(1, 'signal/v1')
sys.path.insert(1, 'pin/v1')

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
Configure digital pin D3 as a digital input
"""
cmd = signal.command
# command message
cmd.type = signal.CMD_TYPE_SET
cmd.name = signal.CMD_NAME_PIN_MODE
# pin message
cmd.pin.name = "D3"
cmd.pin.mode = signal.command.pin.MODE_DIGITAL
cmd.pin.direction = signal.command.pin.DIRECTION_INPUT

print(signal)
signal.Clear()


"""
GET value of pin D3 from Adafruit IO
"""
cmd = signal.command
# command message
cmd.type = signal.CMD_TYPE_GET
cmd.name = signal.CMD_NAME_PIN_VALUE
# pin message
cmd.pin.name = "D3"

print(signal)
signal.Clear()

"""
SET value of pin D3
"""
cmd = signal.command
# command message
cmd.type = signal.CMD_TYPE_GET
cmd.name = signal.CMD_NAME_PIN_VALUE
# pin message
cmd.pin.name = "D3"
cmd.pin.value = "1"

print(signal)
signal.Clear()
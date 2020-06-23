# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')

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
GET library version from adafruit io to the device
"""
command = signal.cmd
# command message
command.type = signal.CMD_MODE_GET
command.name = signal.CMD_NAME_VERSION

print(command)
signal.Clear()


"""
SET library version from device to Adafruit IO
"""
command = signal.cmd
# command message
command.type = signal.CMD_MODE_SET
command.name = signal.CMD_NAME_VERSION
# version message
command.version.major = 1
command.version.minor = 2
command.version.micro = 3

print(command)

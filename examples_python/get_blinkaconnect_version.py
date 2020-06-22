# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT

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

Request library version from device
"""
command = signal.cmd
# command message
command.type = signal.CMD_TYPE_GET
command.name = signal.CMD_NAME_VERSION

print(signal)
serialize_protobuf(signal)
signal.Clear()

"""
PUBLISH from Device to Adafruit IO

Send library version from device to Adafruit IO
"""
command = signal.cmd
# command message
command.type = signal.CMD_TYPE_SET
command.name = signal.CMD_NAME_VERSION

# TODO: This is lacking a way to
# hold the semantic version within signal!

print(signal)
serialize_protobuf(signal)
signal.Clear()
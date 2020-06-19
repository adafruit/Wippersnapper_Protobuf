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
Example: Read digital input, no server-side polling
"""
cmd = signal.pin_cmd
# command message
cmd.command.type = signal.CMD_TYPE_SET
cmd.command.name = signal.CMD_NAME_PIN_MODE
# pin message
cmd.pin = 13
cmd.mode = signal.pin_cmd.PIN_MODE_DIGITAL
cmd.direction = signal.pin_cmd.PIN_DIRECTION_INPUT


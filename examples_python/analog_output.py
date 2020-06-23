# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')

import signal_pb2

# Create new signal message
signal = signal_pb2.Signal()

"""
Configure pin A0 as an analog output
"""
cmd = signal.command
# command message
cmd.mode = signal.CMD_MODE_SET
cmd.name = signal.CMD_NAME_PIN_MODE
# pin message
cmd.pin.name = "A0"
cmd.pin.mode = signal.command.pin.MODE_ANALOG
cmd.pin.direction = signal.command.pin.DIRECTION_OUTPUT

print(signal)
signal.Clear()

"""
Set the value of pin A0
"""
cmd = signal.command
# command message
cmd.mode = signal.CMD_MODE_SET
cmd.name = signal.CMD_NAME_PIN_VALUE
# pin message
cmd.pin.name = "A0"
cmd.pin.value = "512"

print(signal)
signal.Clear()
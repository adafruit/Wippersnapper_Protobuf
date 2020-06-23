# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')

import signal_pb2

# Create new signal message
signal = signal_pb2.Signal()

"""
Configure pin A0 as an ADC input pin
"""
cmd = signal.command
# command message
cmd.mode = signal.CMD_MODE_SET
cmd.type = signal.CMD_TYPE_PIN_MODE
# pin message
cmd.pin.name = "A0"
cmd.pin.mode = signal.command.pin.MODE_ANALOG
cmd.pin.direction = signal.command.pin.DIRECTION_INPUT

print(signal)
signal.Clear()

"""
GET the value from pin A0
"""
cmd = signal.command
# command message
cmd.mode = signal.CMD_MODE_GET
cmd.type = signal.CMD_TYPE_PIN_VALUE
# pin message
cmd.pin.name = "D5"

print(signal)
signal.Clear()

"""
PUBLISH from Adafruit IO to Device

Get the value from an ADC pin
"""
cmd = signal.command
# command message
cmd.mode = signal.CMD_MODE_GET
cmd.type = signal.CMD_TYPE_PIN_VALUE
# pin message
cmd.pin.name = "D5"
cmd.pin.value = "512"

print(signal)
signal.Clear()
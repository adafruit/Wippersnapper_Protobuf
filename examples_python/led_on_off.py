# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT

# Messages transmitted by Adafruit IO
# to toggle a LED on a device


# strict system paths
import sys
sys.path.insert(1, 'semver/v1')
sys.path.insert(1, 'signal/v1')
sys.path.insert(1, 'pin/v1')

import signal_pb2

# Create new signal message
signal = signal_pb2.Signal()

"""
Configure a digital output pin on D13
"""
cmd = signal.command
# command message
cmd.type = signal.CMD_TYPE_SET
cmd.name = signal.CMD_NAME_PIN_MODE
# pin message
cmd.pin.name = "D3"
cmd.pin.mode = signal.command.pin.MODE_DIGITAL
cmd.pin.direction = signal.command.pin.DIRECTION_OUTPUT

print(signal)
signal.Clear()

"""
Turn ON the LED
"""
cmd = signal.command
# command message
cmd.type = signal.CMD_TYPE_SET
cmd.name = signal.CMD_NAME_PIN_VALUE
# pin message
cmd.pin.name = "D13"
cmd.pin.value = "1"

print(signal)
signal.Clear()

"""
Turn OFF the LED
"""
cmd = signal.command
# command message
cmd.type = signal.CMD_TYPE_SET
cmd.name = signal.CMD_NAME_PIN_VALUE
# pin message
cmd.pin.name = "D13"
cmd.pin.value = "0"

print(signal)
signal.Clear()

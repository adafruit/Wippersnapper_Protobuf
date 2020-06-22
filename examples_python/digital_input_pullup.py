# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT

import sys
sys.path.insert(1, 'semver/v1')
sys.path.insert(1, 'signal/v1')
sys.path.insert(1, 'pin/v1')

import signal_pb2

# Create new signal message
signal = signal_pb2.Signal()

"""
PUBLISH from Adafruit IO to Device

Set up digital input on D5 switch with a pull up.
"""
cmd = signal.command
# command message
cmd.type = signal.CMD_TYPE_SET
cmd.name = signal.CMD_NAME_PIN_MODE
# pin message
cmd.pin.name = "D5"
cmd.pin.mode = signal.command.pin.MODE_DIGITAL
cmd.pin.direction = signal.command.pin.DIRECTION_INPUT
cmd.pin.pull = signal.command.pin.PULL_UP

print(signal)
signal.Clear()

"""
GET value of pin D5 from Adafruit IO
"""
cmd = signal.command
# command message
cmd.type = signal.CMD_TYPE_GET
cmd.name = signal.CMD_NAME_PIN_VALUE
# pin message
cmd.pin.name = "D5"

print(signal)
signal.Clear()


"""
PUBLISH from Device to Adafruit IO

Send digital logic level of the pin from the
device to Adafruit IO.
"""
cmd = signal.command
# command message
cmd.type = signal.CMD_TYPE_SET
cmd.name = signal.CMD_NAME_PIN_VALUE
# pin message
cmd.pin.name = "D5"
cmd.pin.value = "1"
print(signal)
signal.Clear()

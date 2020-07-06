# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')

import signal_pb2

# Create new signal message
signal = signal_pb2.Signal()

"""
PUBLISH from Adafruit IO to Device

Set up digital input on D5 switch with a pull up.
"""
# command message
signal.mode = signal.CMD_MODE_SET
signal.type = signal.CMD_TYPE_PIN_MODE
# pin message
signal.pin.name = "D5"
signal.pin.mode = signal.pin.MODE_DIGITAL
signal.pin.direction = signal.pin.DIRECTION_INPUT
signal.pin.pull = signal.pin.PULL_UP

print(signal)
signal.Clear()

"""
GET value of pin D5 from Adafruit IO
"""
# command message
signal.mode = signal.CMD_MODE_GET
signal.type = signal.CMD_TYPE_PIN_VALUE
# pin message
signal.pin.name = "D5"

print(signal)
signal.Clear()


"""
PUBLISH from Device to Adafruit IO

Send digital logic level of the pin from the
device to Adafruit IO.
"""
# command message
signal.mode = signal.CMD_MODE_SET
signal.type = signal.CMD_TYPE_PIN_VALUE
# pin message
signal.pin.name = "D5"
signal.pin.value = "1"
print(signal)
signal.Clear()

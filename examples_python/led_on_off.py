# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')

import signal_pb2

# Create new signal message
signal = signal_pb2.Signal()

"""
Configure a digital output pin on D13
"""
# command message
signal.mode = signal.CMD_MODE_SET
signal.type = signal.CMD_TYPE_PIN_MODE
# pin message
signal.pin.name = "D3"
signal.pin.mode = signal.pin.MODE_DIGITAL
signal.pin.direction = signal.pin.DIRECTION_OUTPUT

print(signal)
signal.Clear()

"""
Turn ON the LED
"""
# command message
signal.mode = signal.CMD_MODE_SET
signal.type = signal.CMD_TYPE_PIN_VALUE
# pin message
signal.pin.name = "D13"
signal.pin.value = "1"

print(signal)
signal.Clear()

"""
Turn OFF the LED
"""
# command message
signal.mode = signal.CMD_MODE_SET
signal.type = signal.CMD_TYPE_PIN_VALUE
# pin message
signal.pin.name = "D13"
signal.pin.value = "0"

print(signal)
signal.Clear()

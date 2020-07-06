# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')

import signal_pb2



"""
Configure pin A0 as an ADC input pin
"""
# Create new signal message
signal = signal_pb2.Signal()
# command message
signal.mode = signal.CMD_MODE_SET
signal.type = signal.CMD_TYPE_PIN_MODE
# pin message
signal.pin.name = "A0"
signal.pin.mode = signal.pin.MODE_ANALOG
signal.pin.direction = signal.pin.DIRECTION_INPUT

print(signal)
signal.Clear()

"""
GET the value from pin A0
"""
# command message
signal.mode = signal.CMD_MODE_GET
signal.type = signal.CMD_TYPE_PIN_VALUE
# pin message
signal.pin.name = "D5"

print(signal)
signal.Clear()

"""
PUBLISH from Adafruit IO to Device

Get the value from an ADC pin
"""
# command message
signal.mode = signal.CMD_MODE_GET
signal.type = signal.CMD_TYPE_PIN_VALUE
# pin message
signal.pin.name = "D5"
signal.pin.value = "512"

print(signal)
signal.Clear()
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
# command message
signal.mode = signal.CMD_MODE_SET
signal.type = signal.CMD_TYPE_PIN_MODE
# pin message
signal.pin.name = "A0"
signal.pin.mode = signal.pin.MODE_ANALOG
signal.pin.direction = signal.pin.DIRECTION_OUTPUT

print(signal)
signal.Clear()

"""
Set the value of pin A0
"""
# command message
signal.mode = signal.CMD_MODE_SET
signal.type = signal.CMD_TYPE_PIN_VALUE
# pin message
signal.pin.name = "A0"
signal.pin.value = "512"

print(signal)
signal.Clear()
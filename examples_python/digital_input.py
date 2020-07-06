# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')

import signal_pb2

# Create new signal message
signal = signal_pb2.Signal()

"""
Configure digital pin D3 as a digital input
"""
# command message
signal.mode = signal.CMD_MODE_SET
signal.type = signal.CMD_TYPE_PIN_MODE
# pin message
signal.pin.name = "D3"
signal.pin.mode = signal.pin.MODE_DIGITAL
signal.pin.direction = signal.pin.DIRECTION_INPUT

print(signal)
signal.Clear()


"""
GET value of pin D3 from Adafruit IO
"""
# command message
signal.mode = signal.CMD_MODE_GET
signal.type = signal.CMD_TYPE_PIN_VALUE
# pin message
signal.pin.name = "D3"

print(signal)
signal.Clear()

"""
SET value of pin D3
"""
# command message
signal.mode = signal.CMD_MODE_GET
signal.type = signal.CMD_TYPE_PIN_VALUE
# pin message
signal.pin.name = "D3"
signal.pin.value = "1"

print(signal)
signal.Clear()
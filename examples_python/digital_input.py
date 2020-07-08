# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')

import signal_pb2

# Create new signal message
signal = signal_pb2.Signal()


# Set up pin D3 as a digital input
signal.mode = signal.CMD_MODE_SET
signal.type = signal.CMD_TYPE_PIN

signal.pin.name = "D3" 
signal.pin.config.mode = signal.pin.config.MODE_DIGITAL
signal.pin.config.direction = signal.pin.config.DIRECTION_INPUT
signal.pin.config.period = 100

print(signal)
signal.Clear()

# Send pin D3 value to Adafruit IO
signal.mode = signal.CMD_MODE_SET
signal.type = signal.CMD_TYPE_PIN
signal.pin.name = "D3"
signal.pin.event.i_val = 1
print(signal)

# TODO: Get Pin value from IO
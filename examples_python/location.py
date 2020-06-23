# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')

import signal_pb2

# Create new signal message
signal = signal_pb2.Signal()

"""
GET device location
"""
cmd = signal.command
# command message
cmd.mode = signal.CMD_MODE_GET
cmd.name = signal.CMD_NAME_LOCATION
print(signal)
signal.Clear()

"""
SET device location
"""
cmd = signal.command
cmd.mode = signal.CMD_MODE_SET
cmd.name = signal.CMD_NAME_LOCATION
# fill location
cmd.location.latitude = 34.211
cmd.location.longitude = -52.91
cmd.location.altitude = 1000

print(signal)
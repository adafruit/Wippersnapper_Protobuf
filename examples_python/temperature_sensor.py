# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')

import signal_pb2

# Create new signal message
signal = signal_pb2.Signal()

"""
Send sensor info to Adafruit IO
"""
cmd = signal.command
cmd.mode = signal.CMD_MODE_SET
cmd.type = signal.CMD_TYPE_SENSOR

# add a new sensor to the command
temperature = cmd.sensors.add()
temperature.type.name = "ADT7410"
temperature.type.sensor_id = 0x01
temperature.type.type = temperature.type.SensorType.            SENSOR_TYPE_AMBIENT_TEMPERATURE = 13;
temperature.type.measurement_period = 0

# NOTE: problem, min of adt7410 is -55C, incomat. type with min value field
temperature.type.min_value = 0

temperature.type.max_value = 150.0
temperature.type.resolution = 0.01

print(cmd)


"""
TODO: Request sensor info from Adafruit IO
"""

"""
TODO: Set up and request multiple sensor information
NOTE: 2x examples for this
"""
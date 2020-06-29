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
temperature.type.type = temperature.type.SensorType.SENSOR_TYPE_AMBIENT_TEMPERATURE = 13;
temperature.type.measurement_period = 0
temperature.type.min_value = -55.0
temperature.type.max_value = 150.0
temperature.type.resolution = 0.01

print(cmd)

signal.Clear()


"""
Send data to Adafruit IO
"""
cmd = signal.command
cmd.mode = signal.CMD_MODE_GET
cmd.type = signal.CMD_TYPE_SENSOR

# add a new sensor to the command
temperature = cmd.sensors.add()
temperature.event.sensor_id = 0x01 # request same sensor identifier
temperature.event.sensor_type = 13
temperature.event.timestamp = 100
temperature.event.temperature = 42

print(cmd)

signal.Clear()

"""
TODO: Set up and request information from multiple types of temperature sensors
NOTE: 2x examples for this
"""
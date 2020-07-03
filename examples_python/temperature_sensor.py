# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')
import signal_pb2

# Create new message
signal = signal_pb2.Signal()

# Set up sensor
cmd = signal.command
cmd.mode = signal.CMD_MODE_SET
cmd.type = signal.CMD_TYPE_SENSOR

# add a new sensor to the command
temperature = cmd.sensor
temperature.type.name = "adt" # sensor's name, as defined in user-code
temperature.type.sensor_id = 0x01 # sensor identifier, automatically incremented in BlinkaConnect library
sensor_type_temp = temperature.SensorType.SENSOR_TYPE_AMBIENT_TEMPERATURE
temperature.type.type = sensor_type_temp # sensor type
temperature.type.measurement_period = 0 # read sensor as quickly as possible
temperature.type.min_value = -55.0 # min value, -55.0C
temperature.type.max_value = 150.0 # max value, 150.0C
temperature.type.resolution = 0.01 # sensor resolution

print(cmd)

signal.Clear()

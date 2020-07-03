# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')
import signal_pb2


# Send message from device advertising a temperature sensor to Adafruit IO
# NOTE: This will create a new `component` on the device's definition
signal = signal_pb2.Signal()
cmd = signal.command
cmd.mode = signal.CMD_MODE_SET
cmd.type = signal.CMD_TYPE_SENSOR
# Configure required sensor properties
cmd.sensor.type.name = "adt"
cmd.sensor.type.sensor_id = 0x01
# Configure optional sensor properties
# TODO: change this to sensor_type
cmd.sensor.type.type = cmd.sensor.SensorType.SENSOR_TYPE_AMBIENT_TEMPERATURE
cmd.sensor.type.measurement_period = 0
cmd.sensor.type.min_value = -55.0
cmd.sensor.type.max_value = 150.0
cmd.sensor.type.resolution = 0.01
print(cmd)
signal.Clear()

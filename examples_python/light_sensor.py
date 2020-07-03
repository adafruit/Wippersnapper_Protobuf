# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')
import signal_pb2

# EXAMPLE: Send message from device advertising a new light sensor to Adafruit IO
# NOTE: This will create a new `component` on the device's definition
signal = signal_pb2.Signal()
cmd = signal.command
cmd.mode = signal.CMD_MODE_SET
cmd.type = signal.CMD_TYPE_SENSOR

light = cmd.sensors.add() # add a light sensor
# Configure required sensor properties
light.type.name = "light"
light.type.sensor_id = 0x01
# Configure optional sensor properties
light.type.sensor_type = light.SensorType.SENSOR_TYPE_LIGHT
light.type.measurement_period = -1
light.type.min_value = 0.0
light.type.max_value = 65535.0

print('* Signal Message \n', signal)
msg = signal.SerializeToString()
print("* Serialized signal message\n", msg)
signal.Clear() # clean up

# EXAMPLE: Send sensor event data from device to Adafruit IO
signal = signal_pb2.Signal()
cmd = signal.command
cmd.mode = signal.CMD_MODE_SET
cmd.type = signal.CMD_TYPE_SENSOR
light = cmd.sensors.add()
light.event.sensor_id = 0x01
light.event.timestamp = 0 # TODO: pull this from cpython timestamp monotonic
light.event.light = 1255.0

print('\n* Signal Message \n', signal)
msg = signal.SerializeToString()
print("* Serialized signal message\n", msg)
signal.Clear() # clean up

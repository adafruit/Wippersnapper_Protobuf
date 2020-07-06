# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')
import signal_pb2

# EXAMPLE: Send message from device advertising a temperature sensor to Adafruit IO
# NOTE: This will create a new `component` on the device's definition
signal = signal_pb2.Signal()
cmd = signal.command
cmd.mode = signal.CMD_MODE_SET
cmd.type = signal.CMD_TYPE_SENSOR

temperature = cmd.sensors.add() # add a temperature sensor
temperature.type.name = "adt"
temperature.type.sensor_id = 0x01
temperature.type.sensor_type = temperature.SENSOR_TYPE_AMBIENT_TEMPERATURE
temperature.type.min_value = -55.0
temperature.type.max_value = 150.0
temperature.type.resolution = 0.01
temperature.type.measurement_period = -1

print('* Signal Message \n', signal)
msg = signal.SerializeToString()
print("* Serialized signal message\n", msg)
signal.Clear() # clean up


# Delete sensor command
signal = signal_pb2.Signal()
cmd = signal.command
cmd.mode = signal.CMD_MODE_DEL
cmd.type = signal.CMD_TYPE_SENSOR

temperature = cmd.sensors.add()
temperature.type.sensor_id = 0x01

print('* Signal Message \n', signal)
msg = signal.SerializeToString()
print("* Serialized signal message\n", msg)
signal.Clear() # clean up

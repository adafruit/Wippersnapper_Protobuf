# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')
import signal_pb2

# Example: Send message from device to Adafruit IO advertising
#           the pyportal's temperature sensor and light sensor.


# TODO HERE!!

# EXAMPLE: Send message from device advertising a temperature sensor to Adafruit IO
# NOTE: This will create a new `component` on the device's definition
signal = signal_pb2.Signal()
cmd = signal.command
cmd.mode = signal.CMD_MODE_SET
cmd.type = signal.CMD_TYPE_SENSOR

temperature = cmd.sensors.add() # add a temperature sensor
temperature.type.name = "adt"
temperature.type.sensor_id = 0x00
temperature.type.sensor_type = temperature.SENSOR_TYPE_AMBIENT_TEMPERATURE
temperature.type.min_value = -55.0
temperature.type.max_value = 150.0
temperature.type.resolution = 0.01
temperature.type.measurement_period = -1

print('* Signal Message \n', signal)
msg = signal.SerializeToString()
print("* Serialized signal message\n", msg)
signal.Clear() # clean up


# EXAMPLE: Send message from device to Adafruit IO on sensor event
cmd = signal.command
cmd.mode = signal.CMD_MODE_SET
cmd.type = signal.CMD_TYPE_SENSOR

temperature = cmd.sensors.add()
temperature.event.sensor_id = 0x00
temperature.event.timestamp = 0
temperature.event.temperature = 32.0

print('\n* Signal Message \n', signal)
msg = signal.SerializeToString()
print("* Serialized signal message\n", msg)
signal.Clear() # clean up
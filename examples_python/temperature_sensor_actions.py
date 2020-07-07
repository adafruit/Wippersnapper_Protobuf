# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')
import signal_pb2

# Example of creating a new temperature sensor component,
# updating the component with a new value, and deleting the component

# CREATE a new temperature sensor component
signal = signal_pb2.Signal()
signal.mode = signal.CmdMode.CMD_MODE_SET
signal.type = signal.CmdType.CMD_TYPE_SENSOR

temperature = signal.sensor
temperature.type.name = "adt"
temperature.type.sensor_id = 0x00
temperature.type.sensor_type = temperature.SENSOR_TYPE_AMBIENT_TEMPERATURE
temperature.type.min_value = -55.0
temperature.type.max_value = 150.0
temperature.type.measurement_period = -1

print('* Creating Sensor...\n', signal)
signal.Clear()
# Update a temperature sensor component with a new temperature value

signal.mode = signal.CmdMode.CMD_MODE_SET
signal.type = signal.CmdType.CMD_TYPE_SENSOR
temperature = signal.sensor
temperature.event.sensor_id = 0x00
temperature.event.timestamp = 0 # TODO: This need to be changed within sensor.proto to a UTC timestamp
temperature.event.temperature = 32.0

print('* Setting temperature value...\n', signal)
signal.Clear()

# Delete a temperature sensor component from a device
signal.mode = signal.CmdMode.CMD_MODE_DEL
signal.type = signal.CmdType.CMD_TYPE_SENSOR

temperature = signal.sensor
temperature.type.sensor_id = 0x01

print('* Deleting temperature sensor component\n', signal)

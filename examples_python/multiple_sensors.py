# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
import sys
sys.path.insert(1, 'signal/v1')
import signal_pb2

# Example: Send message from device to Adafruit IO advertising
#           a PyPortal's temperature sensor and light sensor.
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

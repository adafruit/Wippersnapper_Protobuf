# This code sends messages across a
# signal to set up and turn on/off a LED
# from Adafruit IO to a device

import signal_pb2

signal = signal_pb2.Signal()

# Set pin as digitalio
cmd_pin = signal.cmd_pin
cmd_pin.type = signal.CMD_TYPE_SET
cmd_pin.name = signal.CMD_NAME_PIN_MODE
#TODO: we need a way to do type..
# DigitalInout or Analog or PWM for now
cmd_pin.pin = 13

# Set pin direction
cmd_direction = signal.cmd_pin
cmd_direction.type = signal.CMD_TYPE_SET
# cmd_direction.type = signal.CMD_TYPE_SET
# TODO: Cmd direction!
cmd_direction.pin = 13

# TODO: Serialize and send

# Set pin value to ON
cmd_value = signal.cmd_pin
cmd_value.type = signal.TYPE_SET
cmd_value.name = signal.CMD_NAME_PIN_VALUE
cmd_value.value = "1"
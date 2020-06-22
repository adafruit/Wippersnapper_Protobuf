# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT

# Messages transmitted by Adafruit IO
# to toggle a LED on a device


# strict system paths
import sys
sys.path.insert(1, 'semver/v1')
sys.path.insert(1, 'signal/v1')
sys.path.insert(1, 'pin/v1')
sys.path.insert(1, 'pwm/v1')

import signal_pb2

# Create new signal message
signal = signal_pb2.Signal()

"""
Output a 50% duty cycle on pin D13
"""
cmd = signal.command
# command message
cmd.type = signal.CMD_TYPE_SET
cmd.name = signal.CMD_NAME_PWM_OUTPUT
# pin message
cmd.pwm.pin_name = "D13"
cmd.pwm.duty_cycle = 2 ** 15
cmd.pwm.duty_cycle = 500

print(signal)
signal.Clear()
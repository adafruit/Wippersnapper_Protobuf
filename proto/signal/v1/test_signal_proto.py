import signal_pb2

signal = signal_pb2.Signal()

# add new command to signal
cmd = signal.commands
# pack command 
cmd.type = signal.COMMAND_TYPE_VERSION
cmd.direction = signal.COMMAND_DIRECTION_SET
cmd.value= "0.0.1"

print(signal)
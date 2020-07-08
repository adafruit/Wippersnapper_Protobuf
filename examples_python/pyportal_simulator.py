# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT

# Protobuf imports
import sys
sys.path.insert(1, 'signal/v1')
sys.path.insert(1, 'description/v1')
import signal_pb2
import description_pb2

class BlinkaConnect:
    """Command interface API for Adafruit IO."""
    def __init__(self, device_id, debug=True):
        self.mock_mmqtt_client_iface = None
        self._device_id = device_id
        self._debug = debug
        # Attempt to get_board definition from IO if it exists
        # for the device ID
        definition = self.get_board()
        if not definition:
            print("Could not obtain board definition, attempting to create one...")
        else:
            print("Board definition: ", definition)

    def get_board(self):
        """Returns the board definition as JSON data.
        """
        return True

    def attach_sensor(self, sensor_def):
        """Attaches a new sensor to an Adafruit IO board definition
        """
        pass

    def register_board(self, board_def):
        """Serializes the board definition and sends it to Adafruit IO.
        """
        # TODO: Check if board definition already exists on IO.
        payload = board_def.SerializeToString()
        if self._debug:
            print("Sending board definition to Adafruit IO", payload)

    class Sensor:
        """Provides methods for accessing a sensor component's
        protocol buffer message and related fields.

        """
        pass

    class Board:
        """Provides methods for accessing a board definition
        protocol buffer message and related fields.

        """
        def __init__(self):
            self._board = description_pb2.Description() # init desc. protobuf msg
            self._name = None
            self._version = None
            self._pid = None
            self._vid = None

        def SerializeToString(self):
            return self._board.SerializeToString()
        
        def Clear(self):
            self._board.Clear()

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, name):
            """Sets display name message field.
            :param str display name: User-defined hardware identifier, often the MQTT Client ID.

            """
            self._board.display_name = name

        @property
        def version(self):
            return self._version
        
        @version.setter
        def version(self, version):
            """Sets version message field
            """
            self._board.version.major = int(version.split(".")[0])
            self._board.version.minor = int(version.split(".")[1])
            self._board.version.micro = int(version.split(".")[3])
            self._board.version.label = version.split(".")[2]
        
        @property
        def vid(self):
            return self._vid
        
        @vid.setter
        def vid(self, vid):
            self._board.usb_vid = vid

        @property
        def pid(self):
            return self._pid
        
        @pid.setter
        def pid(self, pid):
            self._board.usb_pid = pid


# initialize BlinkaConnect client
bc = BlinkaConnect()

# create new pyportal
pyportal = bc.Board()
pyportal.display_name = "PyPortal"
# Manufacturer ID
pyportal.vid = 0x239A
pyportal.pid = 0x8036
# Library version
pyportal.version = "0.0.0-alpha.1"

# Serialize the message as a string and send to Adafruit IO
# on `device/ID/description/update` topic
bc.register_board(pyportal)

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
    def __init__(self, board_def):
        self.mock_mmqtt_client_iface = None
        self._board = board_def
    
    def register_board(self):
        """Serializes the board message and displays it as a string.
        """
        payload = self._board.SerializeToString()
        print(payload)


    class Board:
        def __init__(self, pid, vid, version):
            self._board = description_pb2.Description() # init desc. protobuf msg
            self._name = None
            self._version = None
            self._pid = None
            self._vid = None

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
        def version(self, v_major, v_minor, v_micro, v_label):
            """Sets version message field
            :param int v_major: Version major
            :param int v_minor: Version minor
            :param int v_micro: Version patch
            :param str v_micro: Version label

            """
            self._board.version.major = v_major
            self._board.version.v_minor = v_minor
            self._board.version.v_micro = v_micro
            self._board.version.v_label = v_label
        
        @property
        def vid(self):
            return self._vid
        
        @vid.setter
        def vid(self, vid):
            self._board.vid = vid

        @property
        def pid(self):
            return self._pid
        
        @pid.setter
        def pid(self, pid):
            self._board.pid = pid

bc = BlinkaConnect()

# PyPortal Information
__version__ = "0.0.0-alpha.1"
PYPORTAL_VID = 0x239A
PYPORTAL_PID = 0x8036

pyportal = description_pb2.Description()

# User-assigned device name (MQTT Client ID)
pyportal.display_name = "PyPortal"
# PyPortal VID
pyportal.usb_vid = PYPORTAL_VID
# PyPortal PID
pyportal.usb_pid = PYPORTAL_PID

# blinkaconnect code.py version
ver = __version__.split("-")
pyportal.version.major = int(ver[0].split(".")[0])
pyportal.version.minor = int(ver[0].split(".")[1])
pyportal.version.micro = int(ver[0].split(".")[2])
pyportal.version.label = ver[1]

print(pyportal)
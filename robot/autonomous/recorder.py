import wpilib
from magicbot import tunable
import json


class Recorder:
    directory = tunable('')
    recording_name = tunable('')

    frames = []

    def start(self, voltage):
        """
        Start a recording.

        :param voltage: Battery output voltage. Necessary for scaling speeds later on.
        """
        self.voltage = voltage

    def capture(self, joysticks):
        """
        Make snapshot of joystick inputs during this cycle.

        :param joysticks: List of joysticks to read.
        """
        pass

    def stop(self):
        """
        End recording and save data to file.
        """
        pass

import wpilib
from magicbot import tunable
import json
import time


class Recorder:
    """
    Record control input for playback as an autonomous mode.
    """
    directory = tunable('/tmp')
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
        self.frames.append({
            'joysticks': [{
                'axes': [joystick.getRawAxis(axs) for axs in range(joystick.getAxisCount())],
                'buttons': [joystick.getRawButton(btn) for btn in range(joystick.getButtonCount())],
                'pov': [joystick.getPOV(pov) for pov in range(joystick.getPOVCount())],
            } for joystick in joysticks]
        })

    def stop(self):
        """
        End recording and save recorded data to file.
        """
        with open('{directory}/{filename}.json'.format(
                  directory=self.directory,
                  filename=self.recording_name if self.recording_name else int(time.time())), 'w+') as f:
            json.dump({
                'voltage': self.voltage,
                'frames': self.frames,
            }, f)

        self.voltage = None
        self.frames = []

    def execute(self):
        """
        Run periodically when injected through MagicBot.
        """
        pass

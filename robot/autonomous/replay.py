from magicbot.state_machine import state, AutonomousStateMachine
from magicbot import tunable
from networktables.util import ntproperty
from components import drive, arm
import json


class Replay(AutonomousStateMachine):
    """
    Replay recorded control input.
    """
    MODE_NAME = 'Replay'
    DEFAULT = False

    drive: drive.Drive
    arm: arm.Arm

    voltage = ntproperty('/robot/voltage', 1)

    source = tunable('')
    recording = None

    @property
    def compensation(self):
        """
        Get factor by which to multiply motor speeds to account for battery depletion.

        When we replay recorded control input, we'll likely be at a different voltage level
        from when it was recorded.

        :return: Number by which to multiply motor speeds.
        """
        return self.voltage / self.recording['voltage']

    def on_enable(self):
        """
        Read recorded data from file and prepare to run autonomous.
        """
        try:
            with open('/tmp/%s.json' % self.source, 'r') as f:
                self.recording = json.load(f)
        except FileNotFoundError:
            # Terminate autonomous mode
            self.done()
        self.frame = 0

    @state(first=True)
    def run(self):
        """
        Execute recorded instructions.
        """
        # TODO: Rather than manually controlling components, run teleopPeriodic with recorded input.

        self.drive.move(-self.recording['frames'][self.frame]['joysticks'][0]['axes'][1] * self.compensation,
                        self.recording['frames'][self.frame]['joysticks'][1]['axes'][0] * self.compensation)

        if self.recording['frames'][self.frame]['joysticks'][2]['buttons'][1] and not self.recording['frames'][self.frame - 1]['joysticks'][2]['buttons'][1]:
            self.arm.actuate_claw()

        if self.recording['frames'][self.frame]['joysticks'][2]['buttons'][2] and not self.recording['frames'][self.frame - 1]['joysticks'][2]['buttons'][2]:
            self.arm.actuate_forearm()

        self.arm.move(-self.recording['frames'][self.frame]['joysticks'][2]['axes'][1] * self.compensation)

        self.frame += 1
        if self.frame == len(self.recording['frames']):
            self.done()

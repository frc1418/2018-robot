from magicbot.state_machine import state, timed_state, AutonomousStateMachine
from magicbot import tunable
from networktables.util import ntproperty
from components import drive, crane
import json


class Replay(AutonomousStateMachine):
    """
    Replay recorded control input.
    """
    MODE_NAME = 'Replay'
    DEFAULT = False

    drive: drive.Drive
    crane: crane.Crane

    voltage = ntproperty('/robot/voltage', 1)

    source = tunable('')
    recording = None

    @property
    def voltage_multiplier(self):
        """
        Get factor by which to multiply motor speeds to account for battery depletion.

        When we replay recorded control input, we'll likely be at a different voltage level
        from when it was recorded.

        :return: Number by which to multiply motor speeds.
        """
        if self.recording is None:
            return None
        return self.voltage / self.recording['voltage']

    def on_enable(self):
        """
        Read recorded data from file and prepare to run autonomous.
        """
        with open('/tmp/%s.json' % self.source, 'r') as f:
            self.recording = json.load(f)
        self.frame_number = 0

    @state(first=True)
    def run(self):
        """
        Execute recorded instructions.

        TODO: No real reason for this to be stateful.
        """
        # TODO: Rather than manually controlling components, run teleopPeriodic with recorded input.
        fr = self.recording['frames'][self.frame_number]

        self.drive.move(-fr['joysticks'][0]['axes'][1] * self.voltage_multiplier,
                        fr['joysticks'][1]['axes'][0] * self.voltage_multiplier)

        if fr['joysticks'][2]['buttons'][1] and not self.recording['frames'][self.frame_number - 1]['joysticks'][2]['buttons'][1]:
            self.crane.actuate_claw()

        if fr['joysticks'][2]['buttons'][2] and not self.recording['frames'][self.frame_number - 1]['joysticks'][2]['buttons'][2]:
            self.crane.actuate_forearm()

        self.crane.move(-fr['joysticks'][2]['axes'][1] * self.voltage_multiplier)

        self.frame_number += 1
        if self.frame_number == len(self.recording['frames']):
            self.done()

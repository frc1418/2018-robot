from magicbot.state_machine import state, timed_state, AutonomousStateMachine
from magicbot import tunable
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

    recording_name = tunable('')
    frame_number = 0

    @state(first=True)
    def start(self):
        with open('recordings/%s.json' % self.recording_name, 'r') as f:
            self.recording = json.load(f)
        self.next_state('run')

    @timed_state(duration=15)
    def run(self):
        """
        Execute recorded instructions.

        TODO: No real reason for this to be stateful.
        """
        # TODO: Rather than manually controlling components, run teleopPeriodic with recorded input.
        self.frame_number += 1
        fr = self.recording[self.frame_number]

        self.drive.move(-fr['joysticks'][0]['axes'][1], fr['joysticks'][1]['axes'][0])

        if fr['joysticks'][2]['buttons'][1] and not self.recording[self.frame_number - 1]['joysticks'][2]['buttons'][1]:
            self.crane.actuate_claw()

        if fr['joysticks'][2]['buttons'][2] and not self.recording[self.frame_number - 1]['joysticks'][2]['buttons'][2]:
            self.crane.actuate_forearm()

        self.crane.move(-fr['joysticks'][2]['axes'][1])

from magicbot.state_machine import state, timed_state, AutonomousStateMachine
from magicbot import tunable
import json


class Replay(AutonomousStateMachine):
    """
    Replay recorded control input.
    """
    MODE_NAME = 'Replay'
    DEFAULT = False

    recording_name = tunable('')

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
        pass

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
        # TODO: Rather than manually controlling components, find a way to
        # run teleopPeriodic with the recorded input.
        self.frame_number += 1
        fr = self.recording[self.frame_number]

        # TODO: Destroy in fire
        self.drive.move(-fr['joysticks'][0]['axes'][1], fr['joysticks'][1]['axes'][0])

        # TODO: Please never do a git blame
        if fr['joysticks'][2]['buttons'][1] and not self.recording[self.frame_number - 1]['joysticks'][2]['buttons'][1]:
            self.crane.actuate_claw()

        # TODO: There is no elegance here, only sleep deprivation and regret
        if fr['joysticks'][2]['buttons'][2] and not self.recording[self.frame_number - 1]['joysticks'][2]['buttons'][2]:
            self.crane.actuate_forearm()

        self.crane.move(-fr['joysticks'][2]['axes'][1])
        # TODO: H̵̭͕͖̠̳̞͚͞͞É̫̥̺̮̮̻̮͙̩͖͖̭́͟͜͡͠͡ͅC̸̶̨̱̜̘̦̣̯̲̬͎̖̲̟̤̰̤̱̰͟Ǫ̷͍̱̳̬M̶͙̪̮̣͖̰͍͍̮͓̣̜̝̯̼̲̜̭͝E̸̵̯͙̤̯̩̘̱̙̤̦͎̱͍͜͢S̶̢̳̣̤̟̖͓̝͟͢͠ͅͅ

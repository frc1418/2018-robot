from magicbot.state_machine import state, timed_state, AutonomousStateMachine
#from automations import
#from magicbot import tunable
from components import drive


class Charge(AutonomousStateMachine):
    MODE_NAME = 'Charge'
    DEFAULT = True

    drive = drive.Drive

    @timed_state(duration=3, first=True)
    def charge(self, initial_call):
        # Move forward
        self.drive.move(1, 0)

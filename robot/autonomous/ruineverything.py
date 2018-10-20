from magicbot.state_machine import state, timed_state, AutonomousStateMachine
from components import drive
from controllers import motion_profile


class RuinEverything(AutonomousStateMachine):
    """
    Steal everything, kill everyone, cause total financial ruin!
    """
    MODE_NAME = 'RuinEverything'
    DEFAULT = False

    drive = drive.Drive

    @timed_state(duration=8, first=True)
    def charge(self, initial_call):
        # Move forward
        self.drive.move(0.8, 0)

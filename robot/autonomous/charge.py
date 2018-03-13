from magicbot.state_machine import state, timed_state, AutonomousStateMachine
from components import drive
from controllers import motion_profile


class Charge(AutonomousStateMachine):
    MODE_NAME = 'Charge'
    DEFAULT = False

    drive = drive.Drive

    @timed_state(duration=0.8, first=True)
    def charge(self, initial_call):
        # Move forward
        self.drive.move(0.6, 0)


class MotionProfilingTest(AutonomousStateMachine):
    MODE_NAME = 'MotionProfilingTest'
    DEFAULT = True

    pos_controller = motion_profile.PositionController

    @state(first=True)
    def diagonal_move(self, initial_call):
        # Move to a selected waypoint using the pathfinder library
        if initial_call:
            self.pos_controller.move_along('test')

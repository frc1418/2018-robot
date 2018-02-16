from magicbot.state_machine import state, timed_state, AutonomousStateMachine
from components import drive
from controllers import motion_profile


class Charge(AutonomousStateMachine):
    MODE_NAME = 'Charge'
    DEFAULT = True

    drive = drive.Drive

    @timed_state(duration=1, first=True)
    def charge(self, initial_call):
        # Move forward
        self.drive.move(0.6, 0)


class MotionProfilingTest(AutonomousStateMachine):
    MODE_NAME = 'ChargePlanned'
    DEFAULT = False

    position_controller = motion_profile.PositionController()

    @timed_state(duration=3, first=True)
    def diagonal_move(self, initial_call):
        # Move to a selected waypoint using the pathfinder library
        self.position_controller.move_to(4, 4)

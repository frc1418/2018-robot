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

    pos_controller = motion_profile.PositionController

    @state(first=True)
    def diagonal_move(self, initial_call):
        # Move to a selected waypoint using the pathfinder library
        self.pos_controller.move_along('test', True)

        if not self.pos_controller.isRunning('test'):
            self.next_state('stop')

    @state
    def stop(self):
        pass

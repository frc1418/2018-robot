from magicbot.state_machine import state, timed_state, AutonomousStateMachine
#from automations import
#from magicbot import tunable
from components import drive
from magicbot import tunable
from networktables.util import ntproperty


class Modular(AutonomousStateMachine):
    MODE_NAME = 'Modular'
    DEFAULT = False

    drive = drive.Drive

    def initialize(self):
        """
        Set up NetworkTables values on which we will base the auto mode.

        Autonomous configuration data should be input via dashboard.
        """
        self.position = ntproperty('/autonomous/position')
        self.plates = ntproperty('/robot/plates')
        # TODO: This variable is ignored
        # It's not likely we'll ever need to disable advancing,
        # but in theory we should be able to do it.
        self.advance = tunable(True)
        self.drop = tunable(True)

    @state(first=True)
    def start(self):
        """
        Decide how to begin the autonomous.
        """
        # TODO: Decide which method to use to reach switch:
        # gradual turn or move straight forward and turn 90 degrees
        # As of now, we are using gradual turning
        self.next_state('advance_initial')

    # Duration needs to be short so that the robot does not crash into the cube stack if it is in the middle
    @timed_state(duration=0.3, next_state='advance_rotate')
    def advance_initial(self):
        """
        Give the robot some distance from the starting point.
        """
        self.drive.move(0.6, 0)

    @timed_state(duration=0.5, next_state='advance_rotate_final')
    def advance_rotate(self):
        """
        Rotate robot to face the outside of the arena, so it can curve back around.
        """
        # TODO: DRY

        # Numbers are approximate
        if self.position == 'left':
            self.drive.move(0.2, -0.5)
        elif self.position == 'right':
            self.drive.move(0.2, 0.5)
        else:
            if self.plates[0] == 'L':
                self.drive.move(0.2, -0.5)
            elif self.plates[0] == 'R':
                self.drive.move(0.2, 0.5)

    @timed_state(duration=3)
    def advance_rotate_final(self):
        """
        Curve robot around to switch.
        """
        # TODO: DRY
        if self.position == 'left':
            self.drive.move(0.5, 0.5)
        elif self.position == 'right':
            self.drive.move(0.5, -0.5)
        else:
            if self.plates[0] == 'L':
                self.drive.move(0.7, 0.5)
            elif self.plates[0] == 'R':
                self.drive.move(0.7, -0.5)

        if self.drop:
            self.next_state('drop')

    @timed_state(duration=0.5)
    def drop(self):
        """
        Drop preloaded cube in switch.
        """
        # TODO: Complete once manipulator configuration known
        pass

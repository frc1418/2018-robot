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
        self.next_state('advance_initial')

    @timed_state(duration=1, next_state='advance_rotate')
    def advance_initial(self):
        """
        Cross autonomous baseline.
        """
        self.drive.move(1, 0)

    @timed_state(duration=0.3)
    def advance_rotate(self):
        """
        Rotate robot, either to avoid central cube pile or to get to the sides of the switch.
        """
        # TODO: DRY
        if self.position == 'left':
            self.drive.move(0.2, -0.5)
        elif self.position == 'right':
            self.drive.move(0.2, 0.5)
        elif self.position == 'middle':
            if self.plates[0] == 'L':
                self.drive.move(0.2, -0.5)
            elif self.plates[0] == 'R':
                self.drive.move(0.2, 0.5)

        if self.drop:
            self.next_state('drop')

    @timed_state(duration=0.5)
    def drop(self):
        """
        Drop preloaded cube in switch.
        """
        # TODO: Complete once manipulator configuration known
        pass

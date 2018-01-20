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

    @timed_state(duration=0.5, next_state='advance_curve')
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
    def advance_curve(self):
        """
        Curve robot around to switch.
        """
        # TODO: DRY
        if self.position == 'left':
            self.drive.move(0.5, 0.5)
        elif self.position == 'right':
            self.drive.move(0.5, -0.5)
        else:
            # Since the middle position has now reached the same point as either the left or right position,
            # the middle postion is reassigned to either the left or right, depending on its plate
            if self.plates[0] == 'L':
                self.drive.move(0.7, 0.5)
                self.position = 'left'
            elif self.plates[0] == 'R':
                self.drive.move(0.7, -0.5)
                self.position = 'right'

        if self.drop:
            self.next_state('drop_switch')

    @timed_state(duration=0.5)
    def drop_switch(self):
        """
        Drop preloaded cube in switch.
        """
        # TODO: Complete once manipulator configuration known

        next_state('back_up')

    @timed_state(duration=0.3, next_state='pickup_rotate')
    def back_up(self):
        """
        Back up from switch to provide clearance space.
        """
        self.drive.move(-1, 0)

    @timed_state(duration=0.5, next_state='pickup_curve')
    def pickup_rotate(self):
        """
        Rotate into position for the curve method.
        """
        if self.position == 'left':
            self.drive.move(0.2, -0.5)
        if self.position == 'right':
            self.drive.move(0.2, 0.5)

    @timed_state(duration=1)
    def pickup_curve(self):
        """
        Curve into cube so that it is in position for pickup.
        """
        if self.position == 'left':
            self.drive.move(0.7, 0.5)
        elif self.position == 'right':
            self.drive.move(0.7, -0.5)

        self.next_state('pickup_cube')

    @timed_state(duration=1)
    def pickup_cube(self):
        """
        Pick up cube from ground.
        """
        # TODO: Complete once manipulator configuration known

        self.next_state('curve_back')

    @timed_state(duration=1, next_state='rotate_scale')
    def curve_back(self):
        """
        Go back to previous position for easier access to the scale.
        """
        if self.position == 'left':
            self.drive.move(-0.7, 0.5)
        elif self.position == 'right':
            self.drive.move(-0.7, -0.5)

    @timed_state(duration=0.5, next_state='curve_scale')
    def rotate_scale(self):
        """
        Rotate into position to curve into scale.
        """
        if self.position == 'left':
            self.drive.move(0.2, 0.5)
        elif self.position == 'right':
            self.drive.move(0.2, -0.5)

    @timed_state(duration=1)
    def curve_scale(self):
        """
        Curve around to the side of the scale, to get the robot into positon for the scale.
        """
        if self.position == 'left':
            self.drive.move(0.7, -0.5)
        elif self.position == 'right':
            self.drive.move(0.7, -0.5)

        self.next_state('drop_scale')

    @timed_state(duration=0.5)
    def drop_scale(self):
        # TODO: Complete once manipulator configuration known
        pass

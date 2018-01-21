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

    charge = 0.3 # Amount of time robot advances

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
        self.switch = tunable(True)
        self.scale = tunable(True)

    @state(first=True)
    def start(self):
        """
        Decide how to begin the autonomous.
        """

        if self.advance:
            self.next_state('advance_initial')
        # If we are only advancing to cross the auto line,
        # make the charge sequence longer. Only charge if on the left or right,
        # so that the robot will not crash into the switch.
        if not self.switch and not self.scale:
            if self.position == 'left' or self.position == 'right':
                charge = 1.5
        else:
            charge = 0.3

    # Duration needs to be short so that the robot does not crash into the cube stack if it is in the middle
    @timed_state(duration=charge)
    def advance_initial(self):
        """
        Give the robot some distance from the starting point.
        """
        self.drive.move(0.6, 0)
        # Stop here if we are only crossing auto line
        if self.switch or self.scale:
            self.next_state('advance_rotate')

    @timed_state(duration=0.5, next_state='advance_curve')
    def advance_rotate(self):
        """
        Rotate robot to face the outside of the arena, so it can curve back around.
        """
        # TODO: DRY

        # Numbers are approximate
        if self.position == 'left':
            if self.plates[0] == 'L':
                self.drive.move(0.2, -0.5)
            else:
                self.drive.move(0.2, 0.8)
        elif self.position == 'right':
            if self.plates[0] == 'R':
                self.drive.move(0.2, 0.5)
            else:
                self.drive.move(0.2, -0.8)
        else:
            if self.plates[0] == 'L':
                self.drive.move(0.2, -0.5)
            elif self.plates[0] == 'R':
                self.drive.move(0.2, 0.5)
        # The robot will now have the opportunity to pursue different paths
        # It can either try to score on the switch, the switch and the scale,
        # just the scale, or neither, depending on what is selected in the UI
        if self.switch:
            self.next_state('advance_curve')
        # TODO: If only scale is selected and not switch,
        # make a separate state path to go directly to scale
        # elif self.scale:
        #    self.next_state('lorem_ipsum')

    @timed_state(duration=3)
    def advance_curve(self):
        """
        Curve robot around to switch.
        """
        # TODO: DRY
        if self.position == 'left':
            if self.plates[0] == 'L':
                self.drive.move(0.5, 0.5)
            else:
                self.drive.move(0.7, -0.3)
        elif self.position == 'right':
            if self.plates[0] == 'R':
                self.drive.move(0.5, -0.5)
            else:
                self.drive.move(0.7, 0.3)
        else:
            # Since the middle position has now reached the same point as either the left or right position,
            # the middle postion is reassigned to either the left or right, depending on its plate
            if self.plates[0] == 'L':
                self.drive.move(0.6, 0.5)
                self.position = 'left'
            elif self.plates[0] == 'R':
                self.drive.move(0.6, -0.5)
                self.position = 'right'
        self.next_state('advance_curve_final')

    @timed_state(duration=1, next_state='drop_switch')
    def advance_curve_final(self):
        """
        Second part to curving maneuver to curve the robot back into the switch.
        If the robot was already on the correct side of the switch, this second
        state will not take place because it is not needed.
        """
        if self.position == 'left' and self.plates[0] == 'R':
            self.drive.move(0.4, -0.8)
            # Position is now switched
            self.position = 'right'
        elif self.position == 'right' and self.plates[0] == 'L':
            self.drive.move(0.4, 0.8)
            self.position = 'left'

    @timed_state(duration=0.5)
    def drop_switch(self):
        """
        Drop preloaded cube in switch.
        """
        # TODO: Complete once manipulator configuration known
        if self.scale:
            self.next_state('back_up')

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
        Or if the robot is on the wrong side of the scale,
        back up just a little bit
        """
        if self.position == 'left':
            if self.plates[1] == 'L':
                self.drive.move(-0.7, 0.5)
            else:
                self.drive.move(-0.4, 0.5)
        elif self.position == 'right':
            if self.plates[1] == 'R':
                self.drive.move(-0.7, -0.5)
            else:
                self.drive.move(-0.4, 0.5)

    @timed_state(duration=0.5, next_state='curve_scale')
    def rotate_scale(self):
        """
        Rotate into position to curve into scale.
        """
        if self.position == 'left':
            if self.plates[1] == 'L':
                self.drive.move(0.2, 0.5)
            else:
                self.drive.move(0.2, 0.3)
        elif self.position == 'right':
            if self.plates[1] == 'R':
                self.drive.move(0.2, -0.5)
            else:
                self.drive.move(0.2, -0.3)

    @timed_state(duration=1)
    def curve_scale(self):
        """
        Curve around to the side of the scale, to get the robot into positon for the scale.
        """
        if self.position == 'left':
            if self.plates[1] == 'L':
                self.drive.move(0.7, -0.5)
            else:
                self.drive.move(0.4, 0.4)
        elif self.position == 'right':
            if self.plates[1] == 'R':
                self.drive.move(0.7, -0.5)
            else:
                self.drive.move(0.4, -0.4)
        self.next_state('drop_scale')

    @timed_state(duration=0.5)
    def drop_scale(self):
        # TODO: Complete once manipulator configuration known
        pass

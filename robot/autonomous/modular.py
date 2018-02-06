from magicbot.state_machine import state, timed_state, AutonomousStateMachine
from components import drive, crane
from magicbot import tunable
from networktables.util import ntproperty


class Modular(AutonomousStateMachine):
    """
    Modular autonomous.

    Should not be executed on its own.
    """
    DEFAULT = False

    drive = drive.Drive
    crane = crane.Crane

    position = ntproperty('/autonomous/position', '')
    plates = ntproperty('/robot/plates', '')

    switch = tunable(True)
    scale = tunable(False)

    def direction(self):
        """
        Return directional multiplier based on position (or owned plate if in middle position).
        """
        if self.position == 'left':
            return -1
        elif self.postiion == 'right':
            return 1
        else:
            if self.plates[0] == 'L':
                return -1
            if self.plates[0] == 'R':
                return 1

    @state(first=True)
    def start(self):
        """
        Decide how to begin the autonomous.
        """
        self.crane.grip()
        if self.switch:
            if self.position == 'middle':
                self.next_state('switch_middle_start')
            else:
                self.next_state('switch_side_start')

    ########
    # SWITCH
    # SIDE
    ########
    @state
    def switch_side_start(self):
        """
        Initialize switch side autonomous portion.
        """
        self.next_state('switch_side_advance')

    @timed_state(duration=1.7, next_state='switch_side_rotate')
    def switch_side_advance(self):
        """
        Give the robot some distance from the starting point.
        """
        self.crane.move(0.4)
        self.drive.move(0.7, 0)

    @timed_state(duration=0.6, next_state='switch_side_drop')
    def switch_side_rotate(self):
        """
        Rotate robot to face the switch.
        """
        self.crane.move(0.4)
        if self.position == 'left':
            self.drive.move(0.2, 1)
        elif self.position == 'right':
            self.drive.move(0.2, -1)
        else:
            if self.plates[0] == 'L':
                self.drive.move(0.2, -1)
            elif self.plates[0] == 'R':
                self.drive.move(0.2, 1)

    @timed_state(duration=0.5)
    def switch_side_drop(self):
        """
        Drop preloaded cube in switch.
        """
        self.crane.release()

    ########
    # SWITCH
    # MIDDLE
    ########
    @state
    def switch_middle_start(self):
        """
        Set up and start switch autonomous in middle position.
        """
        self.next_state('switch_middle_advance_initial')

    @timed_state(duration=1.0, next_state='switch_middle_advance_final')
    def switch_middle_advance_initial(self):
        """
        Get off wall and turn toward correct goal.
        """
        self.crane.move(0.4)
        self.drive.move(0.6, 1.0 * self.direction())

    @timed_state(duration=1.2, next_state='switch_middle_drop')
    def switch_middle_advance_final(self):
        """
        Turn back to switch and approach.
        """
        self.crane.move(0.4)
        self.drive.move(0.8, -1.0 * self.direction())

    @timed_state(duration=0.5)
    def switch_middle_drop(self):
        """
        Drop in switch from middle position.
        """
        self.crane.release()

from magicbot.state_machine import state, timed_state, AutonomousStateMachine
from components import drive, crane
from magicbot import tunable
from networktables.util import ntproperty

SWITCH = 0
SCALE = 1


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

    # Score on switch?
    switch = tunable(True)
    # Score on scale?
    scale = tunable(False)
    # Decide best scoring option automatically?
    optimize = tunable(False)

    def direction(self, target=0):
        """
        Return directional multiplier based on position (or owned plate if in middle position).

        :param target: ID of target obstacle.
        """
        if self.position == 'left':
            return -1
        elif self.position == 'right':
            return 1
        else:
            if self.plates[target] == 'L':
                return -1
            if self.plates[target] == 'R':
                return 1

    def correct_side(self, target=SWITCH):
        """
        Return whether robot is on correct side to score on given target.

        :param target: ID of target obstacle.
        """
        return (self.direction() == -1 and self.plates[target] == 'L') or (self.direction() == 1 and self.plates[target] == 'R')

    @state(first=True)
    def start(self):
        """
        Decide how to begin the autonomous.
        """
        self.crane.grip()
        self.crane.retract_forearm()
        if self.optimize:
            if self.position == 'middle':
                # If in the middle, score on appropriate side of switch.
                self.next_state('switch_middle_start')
            if self.correct_side(target=SCALE):
                # If we own this side of the scale, score there
                self.next_state('scale_side_start')
            else:
                # If not, score on other side
                self.next_state('switch_side_start')
        if self.switch:
            if self.position == 'middle':
                self.next_state('switch_middle_start')
            else:
                self.next_state('switch_side_start')
        elif self.scale:
            # Assume robot is on side
            self.next_state('scale_side_start')

    ########
    # SWITCH
    # SIDE
    ########
    @state
    def switch_side_start(self):
        """
        Initialize switch side autonomous portion.
        """
        if self.correct_side(target=SWITCH):
            # We are already on the side of the plate we own.
            self.next_state('switch_side_advance')
        else:
            # We'll need to cross the field before dumping our cube.
            self.next_state('switch_side_opposite_advance')

    @timed_state(duration=1.3, next_state='switch_side_rotate')
    def switch_side_advance(self):
        """
        Give the robot some distance from the starting point.
        """
        self.crane.move(0.5)
        self.drive.move(0.7, 0)

    @timed_state(duration=0.6, next_state='switch_side_drop')
    def switch_side_rotate(self):
        """
        Rotate robot to face the switch.
        """
        self.crane.move(0.5)
        self.drive.move(0.2, -1.0 * self.direction())

    @timed_state(duration=0.5, next_state='switch_side_retreat')
    def switch_side_drop(self):
        """
        Drop preloaded cube in switch.
        """
        self.crane.release()

    @timed_state(duration=1.2, next_state='switch_side_second_offwall')
    def switch_side_retreat(self):
        """
        Retreat to side wall.
        """
        self.drive.move(-0.4, 0)

    # FOR SCORING ON OPPOSITE SIDE
    @timed_state(duration=1.7, next_state='switch_side_opposite_rotate')
    def switch_side_opposite_advance(self):
        """
        Give the robot some distance from the starting point.
        """
        self.drive.move(1, 0)

    @timed_state(duration=0.6, next_state='switch_side_opposite_cross')
    def switch_side_opposite_rotate(self):
        """
        Rotate robot to face the opposite wall.
        """
        self.drive.move(0.3, -0.75 * self.direction())

    @timed_state(duration=1.2, next_state='switch_side_opposite_againstwall')
    def switch_side_opposite_cross(self):
        """
        Cross the field to the opposite side of the switch.

        During this state, we should ideally plow into the line of cubes and
        get in position to drop the cube.
        """
        self.drive.move(0.8, 0)

    @timed_state(duration=0.8, next_state='switch_side_opposite_drop')
    def switch_side_opposite_againstwall(self):
        """
        Turn against wall.
        """
        self.crane.move(0.7)
        self.drive.move(0.6, -1 * self.direction())

    @timed_state(duration=0.5)
    def switch_side_opposite_drop(self):
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

    @timed_state(duration=1, next_state='switch_middle_advance_final')
    def switch_middle_advance_initial(self):
        """
        Get off wall and turn toward correct goal.
        """
        self.drive.move(0.6, 0.3 * self.direction())

    @timed_state(duration=1, next_state='switch_middle_drop')
    def switch_middle_advance_final(self):
        """
        Turn back to switch and approach.
        """
        self.crane.move(0.6)
        self.drive.move(0.7, -0.7 * self.direction())

    @timed_state(duration=0.5)
    def switch_middle_drop(self):
        """
        Drop in switch from middle position.
        """
        self.crane.release()

    ########
    # SCALE
    # SIDE
    ########
    @state
    def scale_side_start(self):
        """
        Initialize scale autonomous from side position.
        """
        if self.correct_side(target=SCALE):
            # We are already on the side of the plate we own.
            self.next_state('scale_side_advance')
        else:
            # We'll need to cross the field before dumping our cube.
            self.next_state('scale_side_opposite_advance')

    @timed_state(duration=2, next_state='scale_side_rotate')
    def scale_side_advance(self):
        """
        Advance toward scale.
        """
        self.drive.move(1, 0)

    @timed_state(duration=0.7, next_state='scale_side_windup')
    def scale_side_rotate(self):
        """
        Turn towards scale.
        """
        self.drive.move(0.5, -1 * self.direction())

    @timed_state(duration=1.5, next_state='scale_side_raise')
    def scale_side_windup(self):
        """
        Move backward toward side wall, raising arm.
        """
        self.drive.move(-0.5, 0)

    @timed_state(duration=1.3, next_state='scale_side_approach')
    def scale_side_raise(self):
        """
        Raise arm before scoring.
        """
        self.crane.move(0.65)

    @timed_state(duration=1.3, next_state='scale_side_drop')
    def scale_side_approach(self):
        """
        Approach scale from side before scoring.
        """
        self.crane.extend_forearm()
        self.crane.move(0.2)
        self.drive.move(0.3, 0)

    @timed_state(duration=1, next_state='scale_side_retreat')
    def scale_side_drop(self):
        """
        Drop cube on scale.
        """
        self.crane.move(0.1)
        self.crane.release()

    @timed_state(duration=1, next_state='scale_side_retract')
    def scale_side_retreat(self):
        """
        Retract crane and move away from plate.
        """
        self.drive.move(-0.6, -1.0 * self.direction())
        self.crane.move(0.2)

    @timed_state(duration=2)
    def scale_side_retract(self):
        """
        Move back toward driverstation in preparation for teleop.
        """
        self.crane.retract_forearm()
        self.crane.move(-0.2)

    # FOR SCORING ON OPPOSITE SIDE
    @timed_state(duration=1.75, next_state='scale_side_opposite_rotate')
    def scale_side_opposite_advance(self):
        """
        Give the robot some distance from the starting point.
        """
        self.drive.move(1, 0)

    @timed_state(duration=0.62, next_state='scale_side_opposite_cross')
    def scale_side_opposite_rotate(self):
        """
        Rotate robot to face the opposite wall.
        """
        self.drive.move(0.3, -0.75 * self.direction())

    @timed_state(duration=1.6, next_state='scale_side_opposite_curvein')
    def scale_side_opposite_cross(self):
        """
        Cross the field to the opposite side of the scale.

        During this state, we should ideally plow into the line of cubes and
        get in position to drop the cube.
        """
        self.drive.move(0.8, 0)

    @timed_state(duration=1.6, next_state='scale_side_windup')
    def scale_side_opposite_curvein(self):
        """
        Turn against wall.

        Rather than rewriting the drop process, we'll use this to get into
        position, then begin windup as usual.
        """
        self.drive.move(0.6, 0.7 * self.direction())

from magicbot.state_machine import state, timed_state, AutonomousStateMachine
from components import drive, arm
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
    arm = arm.Arm

    position = ntproperty('/autonomous/position', '')
    plates = ntproperty('/robot/plates', '')

    # Score on switch?
    switch = False
    # Score on scale?
    scale = False
    # Decide best scoring option automatically?
    optimize = False

    def direction(self, target=SWITCH):
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

    def target_direction(self, target=SWITCH):
        """
        Return directional multiplier based on TARGET ownership.

        :param target: ID of target obstacle.
        """
        if self.plates[target] == 'L':
            return -1
        elif self.plates[target] == 'R':
            return 1

    def correct_side(self, target=SWITCH):
        """
        Return whether robot is on correct side to score on given target.

        :param target: ID of target obstacle.
        """
        return (self.direction(target) == -1 and self.plates[target] == 'L') or (self.direction(target) == 1 and self.plates[target] == 'R')

    @state(first=True)
    def start(self):
        """
        Decide how to begin the autonomous.
        """
        if not self.plates:
            self.next_state('charge')
            return
        print('Scale: %r' % self.scale)
        print('Switch: %r' % self.switch)
        print('Optimize: %r' % self.optimize)
        self.arm.grip()
        if self.optimize:
            if self.correct_side(target=SCALE):
                self.next_state('scale_side_start')
            elif self.correct_side(target=SWITCH):
                self.next_state('switch_side_start')
            else:
                if self.scale:
                    self.next_state('scale_side_start')
                elif self.switch:
                    self.next_state('switch_side_start')
                else:
                    self.next_state('charge')
        elif self.switch:
            if self.position == 'middle':
                self.next_state('switch_middle_start')
            else:
                self.next_state('switch_side_start')
        elif self.scale:
            # Assume robot is on side
            self.next_state('scale_side_start')
        else:
            self.next_state('charge')

    @timed_state(duration=1)
    def charge(self):
        # Move forward then stop.
        self.drive.move(0.6, 0)

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

    @timed_state(duration=1.35, next_state='switch_side_rotate')
    def switch_side_advance(self):
        """
        Give the robot some distance from the starting point.
        """
        self.drive.move(0.7, 0)

    @timed_state(duration=0.75, next_state='switch_side_drop')
    def switch_side_rotate(self):
        """
        Rotate robot to face the switch.
        """
        self.arm.move(0.7)
        self.drive.move(0.4, -1.0 * self.direction())

    @timed_state(duration=0.5, next_state='switch_side_retreat')
    def switch_side_drop(self):
        """
        Drop preloaded cube in switch.
        """
        self.arm.release()

    @timed_state(duration=1.6)
    def switch_side_retreat(self):
        """
        Retreat to side wall.
        """
        self.drive.move(-0.3, 0)

    # FOR SCORING ON OPPOSITE SIDE
    @timed_state(duration=1.7, next_state='switch_side_opposite_rotate')
    def switch_side_opposite_advance(self):
        """
        Give the robot some distance from the starting point.
        """
        self.drive.move(1, 0)

    @timed_state(duration=0.6, next_state='switch_side_opposite_precross')
    def switch_side_opposite_rotate(self):
        """
        Rotate robot to face the opposite wall.
        """
        self.drive.move(0.3, -0.9 * self.direction())

    @timed_state(duration=1.7, next_state='switch_side_opposite_cross')
    def switch_side_opposite_precross(self):
        """
        Move back against the wall so we go straight across the field.
        """
        self.drive.move(-0.3, 0)

    @timed_state(duration=1.65, next_state='switch_side_opposite_againstwall')
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
        self.arm.move(0.6)
        self.drive.move(0.5, -0.8 * self.direction())

    @timed_state(duration=0.5)
    def switch_side_opposite_drop(self):
        """
        Drop preloaded cube in switch.
        """
        self.arm.release()

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

    @timed_state(duration=0.8, next_state='switch_middle_advance_final')
    def switch_middle_advance_initial(self):
        """
        Get off wall and turn toward correct goal.
        """
        self.arm.move(0.4)
        self.drive.move(0.7, 0.4 * self.direction())

    @timed_state(duration=1.2, next_state='switch_middle_advance_press')
    def switch_middle_advance_final(self):
        """
        Turn back to switch and approach.
        """
        self.arm.move(0.5)
        self.drive.move(0.4, -(0.2 if self.target_direction(target=SWITCH) == -1 else 0.3) * self.direction())

    @timed_state(duration=0.5, next_state='switch_middle_drop')
    def switch_middle_advance_press(self):
        """
        Press front against switch. This way if we bounce a little we'll still be fine.
        """
        self.arm.move(0.5)
        self.drive.move(0.3, 0)

    @timed_state(duration=0.5)
    def switch_middle_drop(self):
        """
        Drop in switch from middle position.
        """
        self.arm.release()

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

    @timed_state(duration=2.35, next_state='scale_side_rotate')
    def scale_side_advance(self):
        """
        Advance toward scale.
        """
        self.drive.move(1, 0)

    @timed_state(duration=0.5, next_state='scale_side_windup')
    def scale_side_rotate(self):
        """
        Turn towards scale.
        """
        self.drive.move(0.1, -1 * self.direction())

    @timed_state(duration=2.6, next_state='scale_side_raise')
    def scale_side_windup(self):
        """
        Move backward toward side wall, raising arm.
        """
        self.drive.move(-0.2, 0)

    @timed_state(duration=1.6, next_state='scale_side_approach')
    def scale_side_raise(self):
        """
        Raise arm before scoring.
        """
        self.arm.move(0.65)

    @timed_state(duration=1, next_state='scale_side_wait')
    def scale_side_approach(self):
        """
        Approach scale from side before scoring.
        """
        self.arm.extend()
        self.arm.move(0.26)
        self.drive.move(0.3, 0)

    @timed_state(duration=1, next_state='scale_side_drop')
    def scale_side_wait(self):
        """
        Wait for arm to extend.
        """
        pass

    @timed_state(duration=1, next_state='scale_side_retreat')
    def scale_side_drop(self):
        """
        Drop cube on scale.
        """
        self.arm.move(0.1)
        self.arm.release()

    @timed_state(duration=1, next_state='scale_side_retract')
    def scale_side_retreat(self):
        """
        Retract arm and move away from plate.
        """
        # TODO: Check for inversion
        self.drive.move(-0.6, 0.7 * self.target_direction(target=SCALE))
        self.arm.move(0.2)

    @timed_state(duration=2)
    def scale_side_retract(self):
        """
        Move back toward driverstation in preparation for teleop.
        """
        self.arm.retract()
        self.arm.move(-0.2)

    # FOR SCORING ON OPPOSITE SIDE
    @timed_state(duration=1.7, next_state='scale_side_opposite_rotate')
    def scale_side_opposite_advance(self):
        """
        Give the robot some distance from the starting point.
        """
        self.drive.move(1, 0)

    @timed_state(duration=0.6, next_state='scale_side_opposite_precross')
    def scale_side_opposite_rotate(self):
        """
        Rotate robot to face the opposite wall.
        """
        self.drive.move(0.3, -0.9 * self.direction())

    @timed_state(duration=1.7, next_state='scale_side_opposite_cross')
    def scale_side_opposite_precross(self):
        """
        Move back against the wall so we go straight across the field.
        """
        self.drive.move(-0.3, 0)

    @timed_state(duration=1.8, next_state='scale_side_opposite_curvein')
    def scale_side_opposite_cross(self):
        """
        Cross the field to the opposite side of the scale.
        """
        self.drive.move(0.8, 0)

    @timed_state(duration=1.3, next_state='scale_side_windup')
    def scale_side_opposite_curvein(self):
        """
        Turn against wall.

        Continue with normal side scale autonomous rather than duplicating it here.
        """
        self.drive.move(0.8, 0.5 * self.direction())

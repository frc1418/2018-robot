import wpilib
from magicbot import will_reset_to
from magicbot import tunable


class Arm:
    """
    Operate robot arm (all components).
    """
    elevator: wpilib.Victor
    forearm: wpilib.DoubleSolenoid
    claw: wpilib.DoubleSolenoid

    _elevator_speed = will_reset_to(0)

    motion_constant = tunable(0.6)

    def move(self, speed: float):
        """
        Set the motor speed of claw elbow.

        :param speed: The requested speed, between -1 and 1.
        """
        self._elevator_speed = speed

    def up(self):
        """
        Move arm upward.

        Used when controlling arm through buttons.
        """
        self._elevator_speed = 1 * self.motion_constant

    def down(self):
        """
        Move arm downward.

        Used when controlling arm through buttons.
        """
        self._elevator_speed = -1 * self.motion_constant

    def extend(self):
        """
        Extend forearm.
        """
        self.forearm.set(2)

    def retract(self):
        """
        Retract forearm.
        """
        self.forearm.set(1)

    def actuate_forearm(self):
        """
        Extend or retract forearm based on current position.
        """
        self.forearm.set(1 if self.forearm.get() == 2 else 2)

    def grip(self):
        """
        Grip cube in claw.
        """
        self.claw.set(2)

    def release(self):
        """
        Release cube from claw.
        """
        self.claw.set(1)

    def actuate_claw(self):
        """
        Grip or release cube based on current state.
        """
        self.claw.set(1 if self.claw.get() == 2 else 2)

    def execute(self):
        """
        Run elevator motors.
        """
        self.elevator.set(-self._elevator_speed)
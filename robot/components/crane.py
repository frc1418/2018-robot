import wpilib
from magicbot import will_reset_to


class Crane:
    """
    Operate robot arm (all components).
    """
    elevator: wpilib.Victor
    forearm: wpilib.DoubleSolenoid
    claw: wpilib.DoubleSolenoid

    _elevator_speed = will_reset_to(0)

    def elevate(self, speed: float=1):
        """
        Set the motor speed of claw elbow.

        :param speed: The requested speed, between -1 and 1.
        """
        if speed < 0:
            speed /= 2

        self._elevator_speed = speed

    def up(self):
        """
        Move elevator upward.
        """
        self.elevate(1)

    def down(self):
        """
        Move elevator downward.
        """
        self.elevate(-0.5)

    def top(self):
        """
        Move elevator to the topmost position.
        """
        pass

    def bottom(self):
        """
        Move elevator to the bottommost position.
        """
        pass

    def extend_forearm(self):
        """
        Extend forearm.
        """
        self.forearm.set(2)

    def retract_forearm(self):
        """
        Retract forearm.
        """
        self.forearm.set(1)

    def actuate_forearm(self):
        """
        Extend or retract forearm based on current position.
        """
        self.forearm.set(2 if self.forearm.get() == 1 else 1)

    def grip(self):
        """
        Grip cube in claw.
        """
        self.claw.set(1)

    def release(self):
        """
        Release cube from claw.
        """
        self.claw.set(2)

    def actuate_claw(self):
        """
        Grip or release cube based on current state.
        """
        self.claw.set(2 if self.claw.get() == 1 else 1)

    def execute(self):
        """
        Run elevator motors.
        """
        self.elevator.set(self._elevator_speed)

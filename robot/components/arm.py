import wpilib
from magicbot import will_reset_to


class Arm:
    """
    Operate robot arm (all components).
    """
    elevator_motor: wpilib.Victor
    forearm: wpilib.DoubleSolenoid
    hand: wpilib.DoubleSolenoid

    def __init__(self):
        self._elevator_speed = will_reset_to(0)

    def elevate(self, speed: float=1):
        """
        Set the motor speed of arm elbow.

        :param speed: The requested speed, between -1 and 1.
        """
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
        self.elevate(-1)

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
        self.forearm.set(1)

    def retract_forearm(self):
        """
        Retract forearm.
        """
        self.forearm.set(2)

    def actuate_forearm(self):
        """
        Extend or retract forearm based on current position.
        """
        self.forearm.set(2 if self.forearm.get() == 1 else 1)

    def grip(self):
        """
        Grip cube in hand.
        """
        self.hand.set(1)

    def release(self):
        """
        Release cube from hand.
        """
        self.hand.set(2)

    def actuate_forearm(self):
        """
        Grip or release cube based on current state.
        """
        self.hand.set(2 if self.hand.get() == 1 else 1)

    def execute(self):
        """
        Run arm motors.
        """
        self.elevator_motor.set(self._elevator_speed)

import wpilib
from magicbot import will_reset_to


class Arm:
    """
    Operate robot arm (all components).
    """
    elevator_motor: wpilib.Victor

    def __init__(self):
        self._elevator_speed = will_reset_to(0)

    def elevate(self, speed: float=1):
        """
        Set the motor speed of each climbing motor.

        :param speed: The requested speed, between -1 and 1.
        """
        self._elevator_speed = speed

    def ascend(self):
        """
        Move elevator to uppermost possible position.
        """
        pass

    def descend(self):
        """
        Move elevator to bottom.
        """
        pass

    def execute(self):
        """
        Run arm motors.
        """
        self.elevator_motor.set(self._elevator_speed)

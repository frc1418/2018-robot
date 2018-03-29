import wpilib
from magicbot import will_reset_to


class Winch:
    """
    Operate robot winch.
    """
    winch_motors: wpilib.SpeedControllerGroup

    _climb_speed = will_reset_to(0)

    def run(self, speed: float = 1):
        """
        Set the motor speed of each climbing motor.

        :param speed: The requested speed, between -1 and 1.
        """
        self._climb_speed = speed

    def execute(self):
        """
        Run climbing motors.
        """
        self.winch_motors.set(self._climb_speed)

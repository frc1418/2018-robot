import wpilib
from magicbot import will_reset_to


class Winch:
    """
    Operate robot winch.
    """
    winch_motors: wpilib.SpeedControllerGroup
    winch_dog: wpilib.Solenoid

    _climb_speed = will_reset_to(0)

    def run(self, speed: float=1):
        """
        Set the motor speed of each climbing motor.

        :param speed: The requested speed, between -1 and 1.
        """
        self._climb_speed = speed

    # TODO: Check that these states aren't inverted.
    def unlock(self):
        """
        Release dog.
        """
        self.winch_dog.set(False)

    def lock(self):
        """
        Hold dog.
        """
        self.winch_dog.set(True)

    def actuate(self):
        """
        Actuate dog.
        """
        self.winch_dog.set(not self.winch_dog.get())

    def execute(self):
        """
        Run climbing motors.
        """
        self.winch_motors.set(self._climb_speed)

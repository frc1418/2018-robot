import wpilib
from magicbot import will_reset_to


class Winch:
    """
    Operate robot winch.
    """
    winch_motors: wpilib.SpeedControllerGroup
    winch_lock: wpilib.Solenoid

    _climb_speed = will_reset_to(0)

    def run(self, speed: float=1):
        """
        Set the motor speed of each climbing motor.

        :param speed: The requested speed, between -1 and 1.
        """
        self._climb_speed = speed

    def unlock(self):
        """
        Release winch lock.
        """
        self.winch_lock.set(False)

    def lock(self):
        """
        Hold winch lock.
        """
        self.winch_lock.set(True)

    def actuate(self):
        """
        Actuate winch lock.
        """
        self.winch_lock.set(not self.winch_lock.get())

    def execute(self):
        """
        Run climbing motors.
        """
        self.winch_motors.set(self._climb_speed)

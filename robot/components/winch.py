import wpilib
from magicbot import will_reset_to


class Winch:
    """
    Operate robot winch.
    """
    winch_motors: wpilib.SpeedControllerGroup
    winch_hold: wpilib.Solenoid

    def __init__(self):
        self._climb_speed = will_reset_to(0)

    def run(self, speed: float=1):
        """
        Set the motor speed of each climbing motor.

        :param speed: The requested speed, between -1 and 1.
        """
        self._climb_speed = speed

    # TODO: Check that these states aren't inverted.
    def release(self):
        """
        Release winch.
        """
        self.winch_hold.set(False)

    def hold(self):
        """
        Hold winch.
        """
        self.winch_hold.set(True)

    def actuate(self):
        """
        Hold or release winch based on current state.
        """
        self.winch_hold.set(not self.winch_hold.get())

    def execute(self):
        """
        Run climbing motors.
        """
        self.winch_motors.set(self._climb_speed)

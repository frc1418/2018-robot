import wpilib
from magicbot import will_reset_to


class Lift:
    """
    Operate robot lift.
    """
    lift_motor_a: wpilib.Victor
    lift_motor_b: wpilib.Victor

    def __init__(self):
        self._climb_speed = will_reset_to(0)

    def run(self, speed: float):
        """
        Set the motor speed of each climbing motor.

        :param speed: The requested speed, between -1 and 1.
        """
        self._climb_speed = speed

    def execute(self):
        """
        Run climbing motors.
        """
        self.lift_motor_a.set(self._climb_speed)
        self.lift_motor_b.set(self._climb_speed)

import wpilib


class Lift:
    """
    Operate robot lift.
    """
    climb_motor_a: wpilib.Victor
    climb_motor_b: wpilib.Victor

    def __init__(self):
        self._climb_speed = 0

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
        self.climb_motor_a.set(self._climb_speed)
        self.climb_motor_b.set(self._climb_speed)

        self._climb_speed = 0

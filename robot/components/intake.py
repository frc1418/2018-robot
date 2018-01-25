import wpilib
from magicbot import will_reset_to


class Intake:
    """
    Operate robot intake.
    """
    intake_motor_a: wpilib.Victor
    intake_motor_b: wpilib.Victor

    def __init__(self):
        self._intake_speed = will_reset_to(0)

    def move(self, speed: float=1):
        """
        Set the motor speed of intake.

        :param speed: The requested speed, between -1 and 1.
        """
        self._intake_speed = speed

    def open(self):
        """
        Open intake.
        """
        pass

    def close(self):
        """
        Close intake.
        """
        pass

    def actuate(self):
        """
        Open or close intake, depending on current state.
        """
        pass

    def execute(self):
        """
        Run intake motors.
        """
        self.intake_motor_a.set(-self._intake_speed)
        self.intake_motor_a.set(self._intake_speed)

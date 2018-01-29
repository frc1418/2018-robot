import wpilib
from magicbot import will_reset_to


class Intake:
    """
    Operate robot intake.
    """
    shoulders: wpilib.SpeedControllerGroup
    intake_wheels: wpilib.SpeedControllerGroup

    def __init__(self):
        self._shoulder_speed = will_reset_to(0)
        self._intake_wheel_speed = will_reset_to(0)

    def move(self, speed: float=1):
        """
        Set the speed of intake arms.

        :param speed: The requested speed, between -1 and 1.
        """
        self._intake_speed = speed

    def spin(self, speed: float=1):
        """
        Set the speed of intake wheels.

        :param speed: The requested speed, between -1 and 1.
        """
        self._intake_wheel_speed = speed

    def pull(self):
        """
        Pull cube into intake.
        """
        # TODO: Automatically close intake arms if open.
        self.spin(-1)

    def push(self):
        """
        Push cube out of intake.
        """
        self.spin(1)

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
        self.shoulders.set(self._shoulder_speed)
        self.intake_wheels.set(self._intake_wheel_speed)

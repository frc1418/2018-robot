import wpilib
from magicbot import will_reset_to


class Intake:
    """
    Operate robot intake.
    """
    shoulder_left: wpilib.Victor
    shoulder_right: wpilib.Victor
    intake_wheels: wpilib.SpeedControllerGroup

    _shoulder_left_speed = will_reset_to(0)
    _shoulder_right_speed = will_reset_to(0)
    _intake_wheel_speed = will_reset_to(0)

    # TODO: New names
    def move_left(self, speed: float=0.1):
        """
        Set the speed of left intake arm.

        :param speed: The requested speed, between -1 and 1.
        """
        self._shoulder_left_speed = speed

    def move_right(self, speed: float=0.1):
        """
        Set the speed of right intake arm.

        :param speed: The requested speed, between -1 and 1.
        """
        self._shoulder_right_speed = speed

    def spin(self, speed: float=0.5):
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

    def open_left(self):
        """
        Open left side of intake.
        """
        self.move_left(1)

    def open_right(self):
        """
        Open left side of intake.
        """
        self.move_right(1)

    def close_left(self):
        """
        Close left side of intake.
        """
        self.move_left(-1)

    def close_right(self):
        """
        Close right side of intake.
        """
        self.move_right(-1)

    def execute(self):
        """
        Run intake motors.
        """
        self.shoulder_left.set(self._shoulder_left_speed)
        self.shoulder_right.set(self._shoulder_right_speed)
        self.intake_wheels.set(self._intake_wheel_speed)

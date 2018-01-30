import wpilib
import wpilib.drive
from magicbot import will_reset_to


class Drive:
    """
    Handle robot drivetrain.

    All drive interaction must go through this class.
    """
    train: wpilib.drive.DifferentialDrive

    def __init__(self):
        self.enabled = False

    def on_enable(self):
        """
        Tasks for initialization upon injection.
        """
        self.left = will_reset_to(0)
        self.right = will_reset_to(0)

    def move(self, left: float, right: float):
        """
        Move robot.

        :param left: Speed of left side motors.
        :param right: Speed of right side motors.
        """
        self.right = right
        self.left = left

    def execute(self):
        """
        Handle driving.
        """
        self.train.tankDrive(self.left, self.right)

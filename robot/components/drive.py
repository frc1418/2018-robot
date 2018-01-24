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
        self.y = will_reset_to(0)
        self.rotation = will_reset_to(0)

    def move(self, y: float, rotation: float):
        """
        Move robot.

        :param y: y-axis movement speed.
        :param rotation: Rotation speed.
        """
        self.y = y
        self.rotation = rotation

    def execute(self):
        """
        Handle driving.
        """
        self.train.arcadeDrive(self.y, self.rotation)

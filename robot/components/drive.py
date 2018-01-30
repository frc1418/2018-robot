import wpilib
import wpilib.drive
from magicbot import will_reset_to


class Drive:
    """
    Handle robot drivetrain.

    All drive interaction must go through this class.
    """
    train: wpilib.drive.DifferentialDrive

    y = will_reset_to(0)
    rot = will_reset_to(0)

    def __init__(self):
        self.enabled = False
        self.y = will_reset_to(0)
        self.rotation = will_reset_to(0)

    def on_enable(self):
        """
        Tasks for initialization upon injection.
        """
        pass

    def move(self, y: float, rotation: float):
        """
        Move robot.

        :param y: Speed of motion in the y direction. [-1..1]
        :param rot: Speed of rotation. [-1..1]
        """
        self.y = y
        self.rot = rot

    def execute(self):
        """
        Handle driving.
        """
        self.train.arcadeDrive(self.y, self.rot, squaredInputs=False)

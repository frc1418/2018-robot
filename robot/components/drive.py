import wpilib
import wpilib.drive
from magicbot import will_reset_to
from magicbot import tunable


class Drive:
    """
    Handle robot drivetrain.

    All drive interaction must go through this class.
    """
    train: wpilib.drive.DifferentialDrive

    y = will_reset_to(0)
    rot = will_reset_to(0)

    speed_constant = tunable(1.0)
    rotational_constant = tunable(0.5)

    def __init__(self):
        self.enabled = False

    def setup(self):
        """
        Set input threshold.
        """
        self.train.setDeadband(0.1)

    def move(self, y: float, rot: float):
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
        self.train.arcadeDrive(self.speed_constant * self.y,
                               self.rotational_constant * self.rot,
                               squaredInputs=False)

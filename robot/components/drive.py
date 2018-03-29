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
    squared_inputs = tunable(False)

    fine_movement = will_reset_to(False)
    fine_speed_multiplier = tunable(0.5)
    fine_rotation_multiplier = tunable(0.5)

    def __init__(self):
        self.enabled = False

    def setup(self):
        """
        Set input threshold.
        """
        self.train.setDeadband(0.1)

    def move(self, y: float, rot: float, fine_movement: bool = False):
        """
        Move robot.

        :param y: Speed of motion in the y direction. [-1..1]
        :param rot: Speed of rotation. [-1..1]
        :param fine_movement: Decrease speeds for precise motion.
        """
        self.y = y
        self.rot = rot
        self.fine_movement = fine_movement

    def execute(self):
        """
        Handle driving.
        """
        self.train.arcadeDrive(self.speed_constant * self.y * (self.fine_speed_multiplier if self.fine_movement else 1),
                               self.rotational_constant * self.rot * (self.fine_rotation_multiplier if self.fine_movement else 1),
                               squaredInputs=self.squared_inputs)

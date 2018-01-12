import wpilib
import wpilib.drive


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
        self.y = 0
        self.rotation = 0

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

        # Prevent robot from driving by default
        self.y = 0
        self.rotation = 0

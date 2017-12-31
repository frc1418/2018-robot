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
        pass

    def move(self, y: float, rotation: float):
        """
        Move robot.

        :param y: y-axis movement speed.
        :param rotation: Rotation speed.
        """
        pass

    def execute(self):
        """
        Handle driving.
        """
        pass

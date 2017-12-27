import wpilib
import wpilib.drive

from networktables.util import ntproperty


class Drive:
    drive = wpilib.drive.DifferentialDrive

    def __init__(self):
        self.enabled = False

    def on_enable(self):
        pass

    def move(self, y, rotation):
        """
        Move robot.
        """
        pass

    def execute(self):
        """
        Handle driving.
        """
        pass

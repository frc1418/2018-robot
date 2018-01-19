#!/usr/bin/env python3

import magicbot
import wpilib
import wpilib.drive

from ctre.wpi_talonsrx import WPI_TalonSRX


class TestRobot(magicbot.MagicRobot):
    def createObjects(self):
        """
        Initialize testbench components.
        """
        self.lf_motor = WPI_TalonSRX(5)
        self.lr_motor = WPI_TalonSRX(10)
        self.rf_motor = WPI_TalonSRX(15)
        self.rr_motor = WPI_TalonSRX(20)

        self.drive = wpilib.drive.DifferentialDrive(wpilib.SpeedControllerGroup(self.lf_motor, self.lr_motor),
                                                    wpilib.SpeedControllerGroup(self.rf_motor, self.rr_motor))

    def teleopPeriodic(self):
        """
        Spin all motors at full speed.
        """
        self.drive.arcadeDrive(1, 0)


if __name__ == '__main__':
    wpilib.run(TestRobot)

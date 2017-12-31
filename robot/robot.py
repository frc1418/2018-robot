#!/usr/bin/env python3

import magicbot
import wpilib
import wpilib.drive

from robotpy_ext.control.button_debouncer import ButtonDebouncer
from components import drive
#from automations import
#from common import
from magicbot import tunable

from robotpy_ext.common_drivers import navx


class Robot(magicbot.MagicRobot):
    drive = drive.Drive

    def createObjects(self):
        """
        Initialize robot components.
        """
        # Joysticks
        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)

        # TODO: Motors, Drivetrain
        self.lf_motor = wpilib.Victor(0)
        self.lr_motor = wpilib.Victor(1)
        self.rf_motor = wpilib.Victor(2)
        self.rr_motor = wpilib.Victor(3)

        self.train = wpilib.drive.DifferentialDrive(wpilib.SpeedControllerGroup(self.lf_motor, self.lr_motor),
                                                    wpilib.SpeedControllerGroup(self.rf_motor, self.rr_motor))

        # NavX (purple board on top of the RoboRIO)
        self.navx = navx.AHRS.create_spi()

        self.timer = wpilib.Timer()
        self.time = tunable('time')

    def autonomous(self):
        """
        Prepare for and start autonomous mode.
        """
        # Call autonomous
        super().autonomous()

    def disabledInit(self):
        """
        Executed once right away when robot is disabled.
        """
        # Reset Gyro to 0
        self.navx.reset()

    def disabledPeriodic(self):
        """
        Executed periodically while robot is disabled.

        Useful for testing.
        """
        pass

    def teleopInit(self):
        """
        Executed when teleoperated mode begins.
        """
        pass

    def teleopPeriodic(self):
        """
        Executed periodically while robot is in teleoperated mode.
        """
        # Read from joysticks to move drivetrain accordingly
        self.drive.move(-self.joystick_left.getY(), self.joystick_right.getX())

        self.time = self.timer.getMatchTime()


if __name__ == '__main__':
    wpilib.run(Robot)

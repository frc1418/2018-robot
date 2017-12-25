#!/usr/bin/env python3

import magicbot
import wpilib

from robotpy_ext.control.button_debouncer import ButtonDebouncer
from components import drive
#from automations import
#from common import
from networktables.util import ntproperty

from robotpy_ext.common_drivers import navx

from networktables.networktable import NetworkTable


class Robot(magicbot.MagicRobot):
    # TODO: Initialize components

    def createObjects(self):
        """
        Initialize robot components.
        """
        # Joysticks
        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)

        # TODO: Motors, Drivetrain

        # NavX (purple board on top of the RoboRIO)
        self.navx = navx.AHRS.create_spi()

    def autonomous(self):
        """
        Prepare for and start autonomous mode.
        """

        # Reset Gyro to 0
        self.drive.reset_gyro_angle()
        # Call autonomous
        magicbot.MagicRobot.autonomous(self)

    def disabledPeriodic(self):
        """
        Executed periodically while robot is disabled.

        Useful for testing.
        """
        pass

    def disabledInit(self):
        """
        Executed once right away when robot is disabled.
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
        self.drive.move(self.joystick_left.getY(), self.joystick_right.getX())


if __name__ == '__main__':
    wpilib.run(Robot)

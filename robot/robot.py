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
    time = tunable(0)

    def createObjects(self):
        """
        Initialize robot components.
        """
        # Joysticks
        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)

        # Motor controllers
        self.lf_motor = wpilib.Victor(0)
        self.lr_motor = wpilib.Victor(1)
        self.rf_motor = wpilib.Victor(2)
        self.rr_motor = wpilib.Victor(3)

        # Drivetrain object
        self.train = wpilib.drive.DifferentialDrive(wpilib.SpeedControllerGroup(self.lf_motor, self.lr_motor),
                                                    wpilib.SpeedControllerGroup(self.rf_motor, self.rr_motor))

        # NavX (purple board on top of the RoboRIO)
        self.navx = navx.AHRS.create_spi()

        # Utility
        self.ds = wpilib.DriverStation.getInstance()
        self.timer = wpilib.Timer()

    def robotPeriodic(self):
        """
        Executed periodically regardless of mode.
        """
        self.time = int(self.timer.getMatchTime())

    def autonomous(self):
        """
        Prepare for and start autonomous mode.
        """
        # Read data on plate colors from FMS.
        # 3.10: "The FMS provides the ALLIANCE color assigned to each PLATE to the Driver Station software. Immediately following the assignment of PLATE color prior to the start of AUTO."
        # Will fetch a string of three characters ('L' or 'R') denoting position of the current alliance's on the switches and scale, with the nearest structures first.
        # More information: http://wpilib.screenstepslive.com/s/currentCS/m/getting_started/l/826278-2018-game-data-details
        self.plates = list(self.ds.getGameSpecificMessage())

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


if __name__ == '__main__':
    wpilib.run(Robot)

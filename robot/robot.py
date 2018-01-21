#!/usr/bin/env python3

import magicbot
import wpilib
import wpilib.drive

from robotpy_ext.control.button_debouncer import ButtonDebouncer
from components import drive, lift
#from automations import
#from common import
from magicbot import tunable

from robotpy_ext.common_drivers import navx
from ctre.wpi_talonsrx import WPI_TalonSRX

class Robot(magicbot.MagicRobot):
    drive = drive.Drive
    lift = lift.Lift

    time = tunable(0)
    plates = tunable('')

    def createObjects(self):
        """
        Initialize robot components.
        """
        # Joysticks
        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)

        # Motor controllers
        self.lf_motor = WPI_TalonSRX(5)
        self.lr_motor = WPI_TalonSRX(10)
        self.rf_motor = WPI_TalonSRX(15)
        self.rr_motor = WPI_TalonSRX(20)

        # Drivetrain object
        self.train = wpilib.drive.DifferentialDrive(wpilib.SpeedControllerGroup(self.lf_motor, self.lr_motor),
                                                    wpilib.SpeedControllerGroup(self.rf_motor, self.rr_motor))

        # Lift motors
        self.lift_motor_a = wpilib.Victor(0)
        self.lift_motor_b = wpilib.Victor(1)

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

        # Lift
        if self.joystick_left.getRawButton(3) or self.joystick_right.getRawButton(4):
            self.lift.run(-1)
        if self.joystick_right.getRawButton(6):
            self.lift.run(-0.5)


if __name__ == '__main__':
    wpilib.run(Robot)

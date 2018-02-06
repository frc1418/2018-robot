#!/usr/bin/env python3

r"""
   _             _        _              _
  / /\       _  /\ \     / /\          / /\
 / /  \     /\_\\ \ \   / /  \        / /  \
/_/ /\ \   / / / \ \ \ /_/ /\ \      / / /\ \
\_\/\ \ \ / / /   \ \ \\_\/\ \ \    /_/ /\ \ \
     \ \ \\ \ \____\ \ \    \ \ \   \ \ \_\ \ \
      \ \ \\ \________\ \    \ \ \   \ \/__\ \ \
       \ \ \\/________/\ \    \ \ \   \_____\ \ \
      __\ \ \___      \ \ \  __\ \ \___\ \ \_\ \ \
     /___\_\/__/\      \ \_\/___\_\/__/\\ \___\ \ \
     \_________\/       \/_/\_________\/ \_______\/

                           2018 Competition Robot Code
                               Created by FRC Team 1418
                         1418.team // github.com/frc1418
                                                      """

import magicbot
import wpilib
import wpilib.drive

from robotpy_ext.control.button_debouncer import ButtonDebouncer
from components import drive, winch, crane
from controllers import motion_profile
from magicbot import tunable

from robotpy_ext.common_drivers import navx, pressure_sensors
from ctre.wpi_talonsrx import WPI_TalonSRX


class Robot(magicbot.MagicRobot):
    drive: drive.Drive
    winch: winch.Winch
    crane: crane.Crane

    time = tunable(0)
    plates = tunable('')
    pressure = tunable(0)

    def createObjects(self):
        """
        Initialize robot components.
        """
        # Joysticks
        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)
        self.joystick_alt = wpilib.Joystick(2)

        # Buttons
        self.btn_winch_lock = ButtonDebouncer(self.joystick_left, 8)

        # Buttons on alternative joystick
        self.btn_winch_lock_alt = ButtonDebouncer(self.joystick_alt, 8)

        self.btn_claw = ButtonDebouncer(self.joystick_alt, 1)
        self.btn_forearm = ButtonDebouncer(self.joystick_alt, 2)
        self.btn_top = ButtonDebouncer(self.joystick_alt, 6)
        self.btn_bottom = ButtonDebouncer(self.joystick_alt, 4)

        # Drive motor controllers
        # ID SCHEME:
        #   10^1: 1 = left, 2 = right
        #   10^0: 0 = front, 5 = rear
        self.lf_motor = WPI_TalonSRX(10)
        self.lr_motor = WPI_TalonSRX(15)
        self.rf_motor = WPI_TalonSRX(20)
        self.rr_motor = WPI_TalonSRX(25)

        # Drivetrain
        self.train = wpilib.drive.DifferentialDrive(wpilib.SpeedControllerGroup(self.lf_motor, self.lr_motor),
                                                    wpilib.SpeedControllerGroup(self.rf_motor, self.rr_motor))

        # Winch
        self.winch_motors = wpilib.SpeedControllerGroup(wpilib.Victor(7), wpilib.Victor(8))
        self.winch_lock = wpilib.Solenoid(4)

        # Motion Profiling
        self.position_controller = motion_profile.PositionController()

        # Crane
        self.elevator = wpilib.Victor(5)
        self.forearm = wpilib.DoubleSolenoid(2, 3)
        self.claw = wpilib.DoubleSolenoid(0, 1)

        # NavX (purple board on top of the RoboRIO)
        self.navx = navx.AHRS.create_spi()

        # Utility
        self.ds = wpilib.DriverStation.getInstance()
        self.timer = wpilib.Timer()
        self.pressure_sensor = pressure_sensors.REVAnalogPressureSensor(5)
        self.compressor = wpilib.Compressor()

        # Camera server
        wpilib.CameraServer.launch()

    def robotPeriodic(self):
        """
        Executed periodically regardless of mode.
        """
        self.time = int(self.timer.getMatchTime())
        self.pressure = self.pressure_sensor.pressure

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
        # Read from joysticks and move drivetrain accordingly
        self.drive.move(-self.joystick_left.getY(), self.joystick_right.getX())

        # Winch
        if self.joystick_alt.getRawButton(3):
            self.winch.unlock()
            self.winch.run()

        if self.btn_winch_lock.get() or self.btn_winch_lock_alt.get():
            self.winch.lock()

        # Crane
        if self.btn_claw.get():
            self.crane.actuate_claw()

        if self.btn_forearm.get():
            self.crane.actuate_forearm()

        self.crane.move(-self.joystick_alt.getY())


if __name__ == '__main__':
    wpilib.run(Robot)

    print(r"""
     ___      ___ ________  _______
    |\  \    /  /|\   __  \|\  ___ \
    \ \  \  /  / | \  \|\  \ \   __/|
     \ \  \/  / / \ \   __  \ \  \_|/__
      \ \    / /   \ \  \ \  \ \  \_|\ \
       \ \__/ /     \ \__\ \__\ \_______\
        \|__|/       \|__|\|__|\|_______|
             ___      ___ ___  ________ _________  ___  ________
            |\  \    /  /|\  \|\   ____\\___   ___\\  \|\   ____\
            \ \  \  /  / | \  \ \  \___\|___ \  \_\ \  \ \  \___|_
             \ \  \/  / / \ \  \ \  \       \ \  \ \ \  \ \_____  \
              \ \    / /   \ \  \ \  \____   \ \  \ \ \  \|____|\  \
               \ \__/ /     \ \__\ \_______\  \ \__\ \ \__\____\_\  \
                \|__|/       \|__|\|_______|   \|__|  \|__|\_________\
                                                          \|_________|
                                                                    """)

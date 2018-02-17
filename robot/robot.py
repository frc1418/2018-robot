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


class Panthera(magicbot.MagicRobot):
    drive: drive.Drive
    winch: winch.Winch
    crane: crane.Crane

    time = tunable(0)
    plates = tunable('')
    pressure = tunable(0)
    voltage = tunable(0)
    rotation = tunable(0)

    def createObjects(self):
        """
        Initialize robot components.
        """
        # Joysticks
        self.joystick_left = wpilib.Joystick(0)
        self.joystick_right = wpilib.Joystick(1)
        self.joystick_alt = wpilib.Joystick(2)

        # Buttons
        self.btn_claw = ButtonDebouncer(self.joystick_left, 1)
        self.btn_forearm = ButtonDebouncer(self.joystick_right, 1)

        # Buttons on alternative joystick
        self.btn_claw_alt = ButtonDebouncer(self.joystick_alt, 1)
        self.btn_forearm_alt = ButtonDebouncer(self.joystick_alt, 2)

        # Button for toggling unified control
        self.btn_unified_control = ButtonDebouncer(self.joystick_alt, 8)
        self.unified_control = False

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

        # Motion Profiling
        self.position_controller = motion_profile.PositionController()

        # Crane
        self.elevator = wpilib.Victor(5)
        self.forearm = wpilib.DoubleSolenoid(2, 3)
        self.claw = wpilib.DoubleSolenoid(0, 1)

        # NavX (purple board on top of the RoboRIO)
        self.navx = navx.AHRS.create_spi()
        self.navx.reset()

        # Utility
        self.ds = wpilib.DriverStation.getInstance()
        self.timer = wpilib.Timer()
        self.pdp = wpilib.PowerDistributionPanel(0)
        self.pressure_sensor = pressure_sensors.REVAnalogPressureSensor(5)
        self.compressor = wpilib.Compressor()

        # Camera server
        wpilib.CameraServer.launch('camera/camera.py:main')

    def robotPeriodic(self):
        """
        Executed periodically regardless of mode.
        """
        self.time = int(self.timer.getMatchTime())
        self.pressure = self.pressure_sensor.pressure
        self.voltage = self.pdp.getVoltage()
        self.rotation = self.navx.getAngle() % 360

    def autonomous(self):
        """
        Prepare for and start autonomous mode.
        """
        # Read data on plate colors from FMS.
        # 3.10: "The FMS provides the ALLIANCE color assigned to each PLATE to the Driver Station software. Immediately following the assignment of PLATE color prior to the start of AUTO."
        # Will fetch a string of three characters ('L' or 'R') denoting position of the current alliance's on the switches and scale, with the nearest structures first.
        # More information: http://wpilib.screenstepslive.com/s/currentCS/m/getting_started/l/826278-2018-game-data-details
        self.plates = self.ds.getGameSpecificMessage()

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

        if self.btn_unified_control.get():
            self.unified_control = not self.unified_control

        # Winch
        if self.joystick_alt.getRawButton(3) or self.joystick_right.getRawButton(11):
            self.winch.run()

        # Crane
        if (self.btn_claw.get() and self.unified_control) or self.btn_claw_alt.get():
            self.crane.actuate_claw()

        if (self.btn_forearm.get() and self.unified_control) or self.btn_forearm_alt.get():
            self.crane.actuate_forearm()

        self.crane.move(-self.joystick_alt.getY())

        if self.unified_control:
            if self.joystick_right.getRawButton(3):
                self.crane.up()
            if self.joystick_right.getRawButton(2):
                self.crane.down()


if __name__ == '__main__':
    wpilib.run(Panthera)

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

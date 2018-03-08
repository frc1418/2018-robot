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

from wpilib.buttons import JoystickButton
from robotpy_ext.control.button_debouncer import ButtonDebouncer
from components import drive, winch, arm
from controllers import motion_profile, recorder
from magicbot import tunable

from robotpy_ext.common_drivers import navx
from ctre.wpi_talonsrx import WPI_TalonSRX


class Panthera(magicbot.MagicRobot):
    drive: drive.Drive
    winch: winch.Winch
    arm: arm.Arm

    recorder: recorder.Recorder

    time = tunable(0)
    plates = tunable('')
    voltage = tunable(0)
    rotation = tunable(0)

    unified_control = tunable(False)
    recording = tunable(False)
    stabilize = tunable(False)

    stabilizer_threshold = tunable(30)
    stabilizer_aggression = tunable(5)

    fine_rotation_multiplier = tunable(0.5)

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
        self.btn_up = JoystickButton(self.joystick_left, 3)
        self.btn_down = JoystickButton(self.joystick_left, 2)
        self.btn_climb = JoystickButton(self.joystick_right, 11)

        # Buttons on alternative joystick
        self.btn_claw_alt = ButtonDebouncer(self.joystick_alt, 1)
        self.btn_forearm_alt = ButtonDebouncer(self.joystick_alt, 2)
        self.btn_climb_alt = JoystickButton(self.joystick_alt, 3)

        # Buttons for toggling control options and aides
        self.btn_unified_control = ButtonDebouncer(self.joystick_alt, 8)
        self.btn_record = ButtonDebouncer(self.joystick_left, 6)
        self.btn_stabilize = ButtonDebouncer(self.joystick_alt, 12)
        self.btn_fine_rotation = JoystickButton(self.joystick_right, 2)

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

        # Arm
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
        self.compressor = wpilib.Compressor()

        # Camera server
        wpilib.CameraServer.launch('camera/camera.py:main')

    def robotPeriodic(self):
        """
        Executed periodically regardless of mode.
        """
        self.time = int(self.timer.getMatchTime())
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

        self.compressor.stop()

        self.drive.squared_inputs = False
        self.drive.rotational_constant = 0.5

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
        self.compressor.start()

        self.drive.squared_inputs = True
        self.drive.rotational_constant = 0.7

    def teleopPeriodic(self):
        """
        Executed periodically while robot is in teleoperated mode.
        """
        # Read from joysticks and move drivetrain accordingly
        self.drive.move(-self.joystick_left.getY(),
                        self.joystick_right.getX() * (self.fine_rotation_multiplier if self.btn_fine_rotation.get() else 1))

        if self.stabilize:
            if abs(self.navx.getPitch()) > self.stabilizer_threshold:
                self.drive.move(self.navx.getPitch() / 180 * self.stabilizer_aggression, 0)

        if self.btn_stabilize.get():
            self.stabilize = not self.stabilize

        if self.btn_unified_control.get():
            self.unified_control = not self.unified_control

        # Winch
        if (self.btn_climb.get() and self.unified_control) or self.btn_climb_alt.get():
            self.winch.run()

        # Arm
        if (self.btn_claw.get() and self.unified_control) or self.btn_claw_alt.get():
            self.arm.actuate_claw()

        if (self.btn_forearm.get() and self.unified_control) or self.btn_forearm_alt.get():
            self.arm.actuate_forearm()

        self.arm.move(-self.joystick_alt.getY())

        if self.unified_control:
            if self.btn_up.get():
                self.arm.up()
            if self.btn_down.get():
                self.arm.down()

        if self.btn_record.get():
            if self.recording:
                self.recording = False
                self.recorder.stop()
            else:
                self.recording = True
                self.recorder.start(self.voltage)

        if self.recording:
            self.recorder.capture((self.joystick_left, self.joystick_right, self.joystick_alt))


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

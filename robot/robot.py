#!/usr/bin/env python3

import magicbot
import wpilib
import wpilib.drive

from robotpy_ext.control.button_debouncer import ButtonDebouncer
from components import drive, winch, crane, intake
from magicbot import tunable

from robotpy_ext.common_drivers import navx, pressure_sensors
from ctre.wpi_talonsrx import WPI_TalonSRX


class Robot(magicbot.MagicRobot):
    drive = drive.Drive
    winch = winch.Winch
    crane = crane.Crane
    intake = intake.Intake

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
        self.btn_dog = ButtonDebouncer(self.joystick_left, 8)

        self.btn_pull = ButtonDebouncer(self.joystick_left, 2)
        self.btn_push = ButtonDebouncer(self.joystick_left, 3)

        self.btn_claw = ButtonDebouncer(self.joystick_right, 1)
        self.btn_forearm = ButtonDebouncer(self.joystick_right, 5)
        self.btn_top = ButtonDebouncer(self.joystick_right, 3)
        self.btn_bottom = ButtonDebouncer(self.joystick_right, 2)

        # Buttons on alternative joystick
        self.btn_dog_alt = ButtonDebouncer(self.joystick_alt, 8)

        self.btn_claw_alt = ButtonDebouncer(self.joystick_alt, 1)
        self.btn_forearm_alt = ButtonDebouncer(self.joystick_alt, 5)
        self.btn_top_alt = ButtonDebouncer(self.joystick_alt, 6)
        self.btn_bottom_alt = ButtonDebouncer(self.joystick_alt, 4)

        # Drive motor controllers
        # ID SCHEME:
        #   10^1: 1 = left, 2 = right
        #   10^0: 0 = front, 5 = rear
        self.lf_motor = WPI_TalonSRX(10)
        self.lr_motor = WPI_TalonSRX(15)
        self.rf_motor = WPI_TalonSRX(20)
        self.rr_motor = WPI_TalonSRX(25)

        # Configure drive ramp speed
        self.lf_motor.configOpenLoopRamp(0.2, 0)
        self.lr_motor.configOpenLoopRamp(0.2, 0)
        self.rf_motor.configOpenLoopRamp(0.2, 0)
        self.rr_motor.configOpenLoopRamp(0.2, 0)

        # Drivetrain
        self.train = wpilib.drive.DifferentialDrive(wpilib.SpeedControllerGroup(self.lf_motor, self.lr_motor),
                                                    wpilib.SpeedControllerGroup(self.rf_motor, self.rr_motor))

        # Winch
        self.winch_motors = wpilib.SpeedControllerGroup(wpilib.Victor(7), wpilib.Victor(8))
        self.winch_dog = wpilib.Solenoid(4)

        # Crane
        self.elevator_motor = wpilib.Victor(5)
        self.forearm = wpilib.DoubleSolenoid(2, 3)
        self.claw = wpilib.DoubleSolenoid(0, 1)

        # Intake
        self.shoulder_left = wpilib.Victor(6)
        self.shoulder_left.setInverted(True)
        self.shoulder_right = wpilib.Victor(9)

        self.intake_wheel_left = wpilib.Spark(3)
        self.intake_wheel_left.setInverted(True)
        self.intake_wheel_right = wpilib.Spark(4)
        self.intake_wheels = wpilib.SpeedControllerGroup(self.intake_wheel_left,
                                                         self.intake_wheel_right)

        # NavX (purple board on top of the RoboRIO)
        self.navx = navx.AHRS.create_spi()

        # Utility
        self.ds = wpilib.DriverStation.getInstance()
        self.timer = wpilib.Timer()
        self.pressure_sensor = pressure_sensors.REVAnalogPressureSensor(5)

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
        self.drive.move(-self.joystick_left.getY(), -self.joystick_right.getY())

        # Winch
        if self.joystick_left.getRawButton(10) or self.joystick_alt.getRawButton(3):
            self.winch.release()
            self.winch.run()

        if self.btn_dog.get() or self.btn_dog_alt.get():
            self.winch.actuate()

        # Intake
        if self.joystick_left.getRawButton(4) or self.joystick_alt.getRawButton(9):
            self.intake.open()
        elif self.joystick_left.getRawButton(5) or self.joystick_alt.getRawButton(10):
            self.intake.close()

        if self.joystick_left.getRawButton(2) or self.joystick_alt.getRawButton(12):
            self.intake.pull()
        elif self.joystick_left.getRawButton(3) or self.joystick_alt.getRawButton(11):
            self.intake.push()

        # Crane
        if self.btn_claw.get() or self.btn_claw_alt.get():
            self.crane.actuate_claw()

        if self.btn_forearm.get() or self.btn_forearm_alt.get():
            self.crane.actuate_forearm()

        # TODO: Use top()/bottom() rather than up()/down() once encoders present
        # TODO: Remove calls to Joystick.getRawButton()
        if self.btn_top.get() or self.btn_top_alt.get() or self.joystick_right.getRawButton(3) or self.joystick_alt.getRawButton(6):
            # TODO: DRY
            self.crane.retract_forearm()
            self.crane.up()
        elif self.btn_bottom.get() or self.btn_bottom_alt.get() or self.joystick_right.getRawButton(2) or self.joystick_alt.getRawButton(4):
            self.crane.retract_forearm()
            self.crane.down()


if __name__ == '__main__':
    wpilib.run(Robot)

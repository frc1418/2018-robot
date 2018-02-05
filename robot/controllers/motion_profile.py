from collections import deque
from components import drive
from ctre import WPI_TalonSRX
from math import radians
import pathfinder as pf
from robotpy_ext.common_drivers import navx
from threading import Lock, Condition, Thread
import time
import wpilib

# TODO Get actual values
ENCODER_TICKS = 1023
WHEEL_DIAMETER = 7.639
MAX_VELOCITY = 25


class PositionController:
    """
    Controls the position of the robot using motion profile based movement.
    """
    lf_motor = WPI_TalonSRX
    lr_motor = WPI_TalonSRX
    rf_motor = WPI_TalonSRX
    rr_motor = WPI_TalonSRX
    navx = navx

    def __init__(self):
        self.trajectories = deque()

        self.right_follower = None
        self.left_follower = None

        self.lock = Lock()
        self.cond = Condition(self.lock)
        self.thread = Thread(target=self._run, daemon=True)
        self.thread.start()

        self.motors = [
            self.lf_motor,
            self.lr_motor,
            self.rf_motor,
            self.rr_motor
        ]

        wpilib.Resource._add_global_resource(self)

    def move_to(self, x_position, y_position, angle=0, first=False):
        """
        Generate path and set path variable

        :param x_position: The x distance.
        :param y_position: The y distance.
        :param angle: The angle difference in degrees.
        :param first: Whether or not this path should be completed next.
        """
        waypoint = pf.Waypoint(float(x_position),
                               float(y_position), radians(angle))

        info, trajectory = pf.generate([pf.Waypoint(0, 0, 0), waypoint],
                                       pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH,
                                       0.05, 1.7, 2.0, 60.0)

        modifier = pf.modifiers.TankModifier(trajectory).modify(0.5)
        right_trajectory = modifier.getRightTrajectory()
        left_trajectory = modifier.getLeftTrajectory()

        with self.cond:
            if self.left_follower or self.right_follower is None:
                self.right_follower = pf.followers.EncoderFollower(right_trajectory)
                self.left_follower = pf.followers.EncoderFollower(left_trajectory)

                right_pos = self.rf_motor.getQuadraturePosition()
                left_pos = self.lf_motor.getQuadraturePosition()

                self.right_follower.configureEncoder(right_pos, ENCODER_TICKS, WHEEL_DIAMETER)
                self.left_follower.configureEncoder(left_pos, ENCODER_TICKS, WHEEL_DIAMETER)

                self.right_follower.configurePIDVA(1.0, 0.0, 0.0, 1 / MAX_VELOCITY, 0)
                self.left_follower.configurePIDVA(1.0, 0.0, 0.0, 1 / MAX_VELOCITY, 0)

            if first:
                self.trajectories.appendLeft({'right': right_trajectory,
                                              'left': left_trajectory})
            else:
                self.trajectories.append({'right': right_trajectory, 'left': left_trajectory})

        self.cond.notify()

    def _run(self):
        """
        Actually move the robot along the path.
        """
        while True:
            with self.cond:
                if len(self.trajectories) < 1:
                    self.cond.wait_for(lambda: len(self.trajectories) > 0)

                if self.right_follower.isFinished() and self.left_follower.isFinished():
                    trajectory = self.trajectories.popleft()
                    self.right_follower.setTrajectory(trajectory['right'])
                    self.left_follower.setTrajectory(trajectory['left'])
                else:
                    right = self.right_follower.calculate(self.rf_motor.getQuadraturePosition)
                    left = self.left_follower.calculate(self.lf_motor.getQuadraturePosition())

                    gyro_heading = self.navx.getAngle()
                    desired_heading = math.degrees(self.left_follower.getHeading())

                    angleDifference = self._bound_half_degrees(desired_heading - gyro_heading)
                    turn = 0.8 * (-1.0 / 80.0) * angleDifference

                    for i, motor in enumerate(self.motors):
                        if i < 2:
                            motor.set(left + turn)
                        else:
                            motor.set(right - turn)

    def _bound_half_degrees(self, angle_degrees):
        """
        Python implementation of pathfinder boundHalfDegrees method.

        :param angle_degrees: Degrees to bind.
        """
        while angle_degrees >= 180.0:
            angle_degrees -= 360.0
        while angle_degrees < -180.0:
            angle_degrees += 360.0

        return angle_degrees

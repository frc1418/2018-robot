from collections import deque
from components import drive
from math import radians, degrees
import pathfinder as pf
from threading import Lock, Condition, Thread
import time
import wpilib

# TODO Get actual values
MAX_VELOCITY = 200

TIME_DIFF = 0.05
# TODO
# Also add a file + class to generate trajectories in multiple threads. (or 1)
# Save these trajectories to files or have them generate when robot is disabled


class PositionController:
    """
    Controls the position of the robot using motion profile based movement.
    """

    def __init__(self, lf_motor, lr_motor, rf_motor, rr_motor, navx, right_encoder, left_encoder):
        """
        :param lf_motor: The left front motor
        :param lr_motor: The left rear motor
        :param rf_motor: The right front motor
        :param rr_motor: The right rear motor
        :param navx: The navx
        :param right_encoder: Right encoder which hooks into right front motor
        :param left_encoder: Left encoder which hooks into left front motor
        """
        self.trajectories = deque()

        self.right_follower = None
        self.left_follower = None

        self.right_encoder = right_encoder
        self.left_encoder = left_encoder

        self.navx = navx

        self.lock = Lock()
        self.cond = Condition(self.lock)
        self.thread = Thread(target=self._control_loop, daemon=True)
        self.thread.start()

        self.motors = [
            lf_motor,
            lr_motor,
            rf_motor,
            rr_motor
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
                                       TIME_DIFF, 1.7, 2.0, 60.0)

        modifier = pf.modifiers.TankModifier(trajectory).modify(0.6)
        right_trajectory = modifier.getRightTrajectory()
        left_trajectory = modifier.getLeftTrajectory()

        with self.cond:
            if self.left_follower or self.right_follower is None:
                self.right_follower = pf.followers.DistanceFollower(right_trajectory)
                self.left_follower = pf.followers.DistanceFollower(left_trajectory)

                self.right_follower.configurePIDVA(1.0, 0.0, 0.0, 1 / MAX_VELOCITY, 0)
                self.left_follower.configurePIDVA(1.0, 0.0, 0.0, 1 / MAX_VELOCITY, 0)

            if first:
                self.trajectories.appendLeft({'right': right_trajectory,
                                              'left': left_trajectory})
            else:
                self.trajectories.append({'right': right_trajectory, 'left': left_trajectory})

            self.cond.notify()

    def _control_loop(self):
        """
        Actually move the robot along the path.
        """
        while True:
            with self.cond:
                if len(self.trajectories) < 1:
                    self.cond.wait_for(lambda: len(self.trajectories) > 0)

                if self.right_follower.isFinished() and self.left_follower.isFinished():
                    del self.trajectories[0]
                    if len(self.trajectories) < 1:
                        continue

                    trajectory = self.trajectories[0]

                    self.right_follower.setTrajectory(trajectory['right'])
                    self.left_follower.setTrajectory(trajectory['left'])
                else:
                    right = self.right_follower.calculate(self.right_encoder.getDistance())
                    left = self.left_follower.calculate(self.left_encoder.getDistance())

                    gyro_heading = self.navx.getAngle()
                    desired_heading = degrees(self.left_follower.getHeading())

                    angleDifference = self._bound_half_degrees(desired_heading - gyro_heading)
                    turn = 0.8 * (-1.0 / 80.0) * angleDifference

                    for i, motor in enumerate(self.motors):
                        if i < 2:
                            motor.set(left + turn)
                        else:
                            motor.set(right - turn)
                    time.sleep(TIME_DIFF)

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

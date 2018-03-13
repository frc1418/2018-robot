from collections import deque
from components import drive
from ctre import TalonSRX
import pathfinder as pf
from .profile_generator import ProfileGenerator
from robotpy_ext.misc.precise_delay import PreciseDelay
from threading import Lock, Condition, Thread
import wpilib
import time

MAX_VELOCITY = 9
ENCODER_TICKS = 360
WHEEL_DIAMETER = 0.5


class PositionController:
    """
    Controls the position of the robot using motion profile based movement.
    """

    def __init__(self, lf_motor: TalonSRX, lr_motor, rf_motor, rr_motor, navx, drive, r_encoder, l_encoder):
        """
        :param lf_motor: The left front motor (Annotated for autocompletion)
        :param lr_motor: The left rear motor
        :param rf_motor: The right front motor
        :param rr_motor: The right rear motor
        :param navx: The navx
        :param drive: Drive system for the robot
        :param r_encoder: The right encoder on the robot
        :param l_encoder: The left encoder on the robot
        """
        self.disabled = True
        self.profile_generator = ProfileGenerator()
        self.queued_trajectories = deque()
        self.current_trajectory = None

        self.navx = navx

        self.left_follower = None
        self.right_follower = None
        self.drive = drive
        self.right_encoder = r_encoder
        self.left_encoder = l_encoder

        self.lock = Lock()
        self.cond = Condition(self.lock)
        self.thread = Thread(target=self._control_loop, daemon=True)
        self.thread.start()
        self.stop = False

        self.motors = [
            lf_motor,
            lr_motor,
            rf_motor,
            rr_motor
        ]

        wpilib.Resource._add_global_resource(self)

    def move_along(self, trajectory_name, first=False):
        """
        Generate path and set path variable

        :param trajectory_name: The name of the pre-generated trajectory.
        :param first: Whether or not this path should be completed next.
        """
        if trajectory_name not in self.possible_trajectories.keys():
            raise KeyError('The trajectory you specified could not be found.')

        trajectory = self.possible_trajectories[trajectory_name]

        if self.left_follower is None or self.right_follower is None:
            self.right_follower = pf.followers.EncoderFollower(trajectory[0])
            self.left_follower = pf.followers.EncoderFollower(trajectory[1])

        if first:
            self.queued_trajectories.appendLeft(trajectory)
        else:
            self.queued_trajectories.append(trajectory)

        with self.cond:
            self.disabled = False
            self.cond.notify()

    def _control_loop(self):
        """
        Pushes trajectory points to the TalonSRX top level buffer
        """
        delay = PreciseDelay(0.05)
        while True:
            with self.cond:
                self.cond.wait_for(lambda: not self.disabled)

                if self.current_trajectory is None:
                    self.cond.wait_for(lambda: len(self.queued_trajectories) > 0)

                    self.current_trajectory = self.queued_trajectories.popleft()
                    self.right_follower.setTrajectory(self.current_trajectory[0])
                    self.left_follower.setTrajectory(self.current_trajectory[1])
                    self.configure_followers()

                elif self.left_follower.isFinished() and self.right_follower.isFinished():
                    self.current_trajectory = None
                    continue

            left_ouput = self.left_follower.calculate(self.left_encoder.get())
            right_output = self.right_follower.calculate(self.right_encoder.get())

            gyro_heading = None
            if self.stop:
                gyro_heading = -(self.navx.getAngle() % 360)

            if gyro_heading is None:
                return
            desired_heading = pf.r2d(self.left_follower.getHeading())

            angleDifference = pf.boundHalfDegrees(desired_heading - gyro_heading)
            turn = 5 * (-1.0 / 80.0) * angleDifference

            left_ouput = left_ouput + turn
            right_output = right_output - turn

            self.drive.tankDrive(-left_ouput, -right_output)
            delay.delay(0.05)

    def prepare(self):
        """
        Prepare to generate the trajectories
        """
        self.profile_generator.generate_all_lists()
        self.possible_trajectories = self.profile_generator.trajectories

    def free(self):
        """
        Free the control loop thread
        """
        self.thread.stop = True

    def configure_followers(self):
        """
        Configure the followers for another trajectory.
        """
        self.left_follower.configureEncoder(self.left_encoder.get(), ENCODER_TICKS, WHEEL_DIAMETER)
        self.right_follower.configureEncoder(self.right_encoder.get(), ENCODER_TICKS, WHEEL_DIAMETER)
        self.right_follower.configurePIDVA(1.0, 0.0, 0.0, 1 / MAX_VELOCITY, 0)
        self.left_follower.configurePIDVA(1.0, 0.0, 0.0, 1 / MAX_VELOCITY, 0)

    def isRunning(self, trajectory_name):
        """
        Check if a certain trajectory is currently running.

        :param trajectory_name: The name of the trajectory to check.
        """
        with self.cond:
            queue_first = None if len(self.queued_trajectories) < 1 else self.queued_trajectories[0]
            current = self.current_trajectory
        return (current == self.possible_trajectories[trajectory_name] or
                self.possible_trajectories[trajectory_name] == queue_first)

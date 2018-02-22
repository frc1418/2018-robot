from collections import deque
from components import drive
from ctre import wpi_talonsrx, talonsrx, trajectorypoint
import pathfinder as pf
from .profile_generator import ProfileGenerator
from robotpy_ext.misc.precise_delay import PreciseDelay
from threading import Lock, Condition, Thread
import wpilib

MAX_VELOCITY = 7
ENCODER_TICKS = 1440
WHEELBASE_WIDTH = 1.6
WHEEL_DIAMETER = 0.152


class PositionController:
    """
    Controls the position of the robot using motion profile based movement.
    """

    def __init__(self, lf_motor: wpi_talonsrx.TalonSRX, lr_motor, rf_motor, rr_motor, navx, right_encoder, left_encoder):
        """
        :param lf_motor: The left front motor (Annotated for autocompletion)
        :param lr_motor: The left rear motor
        :param rf_motor: The right front motor
        :param rr_motor: The right rear motor
        :param navx: The navx
        :param right_encoder: The right front Encoder
        :param left_encoder: The left front Encoder
        """
        self.disabled = True
        self.profile_generator = ProfileGenerator()
        self.queued_trajectories = deque()
        self.current_trajectory = None

        self.navx = navx

        self.left_encoder = left_encoder
        self.right_encoder = right_encoder
        self.left_follower = None
        self.right_follower = None

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

        for motor in self.motors:
            motor.configSelectedFeedbackSensor(talonsrx.TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)

    def move_along(self, trajectory_name, first=False):
        """
        Generate path and set path variable

        :param trajectory_name: The name of the pre-generated trajectory.
        :param first: Whether or not this path should be completed next.
        """
        self.disabled = False
        if trajectory_name not in self.possible_trajectories.keys():
            raise KeyError('The trajectory you specified could not be found.')

        trajectory = self.possible_trajectories[trajectory_name]

        if self.left_follower is None or self.right_follower is None:
            self.right_follower = pf.followers.EncoderFollower(trajectory[0])
            self.left_follower = pf.followers.EncoderFollower(trajectory[1])

            self.right_follower.configurePIDVA(1, 0, 0, 1 / MAX_VELOCITY, 0)
            self.left_follower.configurePIDVA(1, 0, 0, 1 / MAX_VELOCITY, 0)

        with self.cond:
            if first:
                self.queued_trajectories.appendLeft(trajectory)
            else:
                self.queued_trajectories.append(trajectory)
            self.cond.notify()

    def _control_loop(self):
        """
        Pushes trajectory points to the TalonSRX top level buffer
        """
        delay = PreciseDelay(self.profile_generator.TIME_DIFF)
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

                left_ouput = self.left_follower.calculate(self.motors[0].getQuadraturePosition())
                right_output = self.right_follower.calculate(self.motors[1].getQuadraturePosition())

                gyro_heading = self.navx.getAngle() % 360
                desired_heading = pf.r2d(self.left_follower.getHeading())

                angleDifference = pf.boundHalfDegrees(desired_heading - gyro_heading)
                turn = 0.8 * (-1.0 / 80.0) * angleDifference

                for i, motor in enumerate(self.motors):
                    if i < 2:
                        motor.set(left_ouput + turn)
                    else:
                        motor.set(right_output - turn)

                delay.wait()

    def prepare(self):
        """
        Prepare to generate the trajectories
        """
        self.profile_generator.generate_all_lists()
        self.possible_trajectories = self.profile_generator.trajectories

    def configure_followers(self):
        """
        Configure the followers for another trajectory.
        """
        self.left_encoder.reset()
        self.right_encoder.reset()
        self.left_follower.configureEncoder(self.motors[0].getQuadraturePosition(), ENCODER_TICKS, WHEEL_DIAMETER)
        self.right_follower.configureEncoder(self.motors[1].getQuadraturePosition(), ENCODER_TICKS, WHEEL_DIAMETER)

    def isRunning(self, trajectory_name):
        """
        Check if a certain trajectory is currently running.

        :param trajectory_name: The name of the trajectory to check.
        """
        queue_first = None if len(self.queued_trajectories) < 1 else self.queued_trajectories[0]
        return (self.current_trajectory == self.possible_trajectories[trajectory_name] or
                self.possible_trajectories[trajectory_name] == queue_first)

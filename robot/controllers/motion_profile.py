from collections import deque
from components import drive
from ctre import wpi_talonsrx, talonsrx, trajectorypoint
import pathfinder as pf
from .profile_generator import ProfileGenerator
from robotpy_ext.misc.precise_delay import PreciseDelay
from threading import Lock, Condition, Thread
import wpilib

MAX_VELOCITY = 11


class PositionController:
    """
    Controls the position of the robot using motion profile based movement.
    """

    def __init__(self, lf_motor: wpi_talonsrx.TalonSRX, lr_motor, rf_motor, rr_motor, navx):
        """
        :param lf_motor: The left front motor (Annotated for autocompletion)
        :param lr_motor: The left rear motor
        :param rf_motor: The right front motor
        :param rr_motor: The right rear motor
        :param navx: The navx
        """
        self.disabled = True
        self.profile_generator = ProfileGenerator()
        self.queued_trajectories = deque()
        self.current_trajectory = None

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

        for motor in self.motors:
            motor.configMotionProfileTrajectoryPeriod(0, 50)
            motor.configSelectedFeedbackSensor(talonsrx.TalonSRX.FeedbackDevice.QuadEncoder, 0, 0)

        self.notifier = wpilib.Notifier(run=self._push_trajectory)

        wpilib.Resource._add_global_resource(self)

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
        current_segment = 0
        segments = None
        delay = PreciseDelay(self.profile_generator.TIME_DIFF)
        while True:
            with self.cond:
                self.cond.wait_for(lambda: not self.disabled)

                if self.current_trajectory is None:
                    for motor in self.motors:
                        motor.set(talonsrx.TalonSRX.ControlMode.PercentOutput, 0)

                    self.cond.wait_for(lambda: len(self.queued_trajectories) > 0)

                    for motor in self.motors:
                        motor.set(talonsrx.TalonSRX.ControlMode.MotionProfile, 1)
                    self.current_trajectory = self.queued_trajectories.popleft()
                    segments = list(zip(self.current_trajectory[0], self.current_trajectory[1]))

                is_last = False
                if current_segment == 0:
                    first = segments[0]
                    last = segments[-1]

                if current_segment == len(segments) - 1:
                    is_last = True
                elif current_segment >= len(segments):
                    for motor in self.motors:
                        motor.set(talonsrx.TalonSRX.ControlMode.MotionProfile, 0)
                        motor.clearMotionProfileTrajectories()

                    self.current_trajectory = None
                    current_segment = 0
                    first = None
                    last = None
                    segments = None
                    continue

                seg = segments[current_segment]
                right_point = trajectorypoint.TrajectoryPoint(seg[0].position, seg[0].velocity,
                                                              seg[0].heading, 0, 1, is_last, first[0] == seg[0],
                                                              int(self.profile_generator.TIME_DIFF * 1000))

                left_point = trajectorypoint.TrajectoryPoint(seg[1].position, seg[1].velocity,
                                                             seg[1].heading, 0, 1, is_last, first[1] == seg[1],
                                                             int(self.profile_generator.TIME_DIFF * 1000))

                for i, motor in enumerate(self.motors):
                    if i < 2:
                        motor.pushMotionProfileTrajectory(left_point)
                    else:
                        motor.pushMotionProfileTrajectory(right_point)

                current_segment += 1
                delay.wait()

    def prepare(self):
        """
        Prepare to generate the trajectories
        """
        self.profile_generator.generate_all_lists()
        self.possible_trajectories = self.profile_generator.trajectories
        self.notifier.startPeriodic(self.profile_generator.TIME_DIFF / 2)

    def _push_trajectory(self):
        """
        Push trajectories from the TalonSRX top to lower buffer.
        """
        if not self.disabled and self.current_trajectory is not None:
            for motor in self.motors:
                motor.processMotionProfileBuffer()

    def isRunning(self, trajectory_name):
        """
        Check if a certain trajectory is currently running.

        :param trajectory_name: The name of the trajectory to check.
        """
        queue_first = None if len(self.queued_trajectories) < 1 else self.queued_trajectories[0]
        return (self.current_trajectory == self.possible_trajectories[trajectory_name] or
                self.possible_trajectories[trajectory_name] == queue_first)

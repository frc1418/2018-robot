import wpilib
from components import drive
import pathfinder as pf
import math
from collections import deque
import threading


class PositionController:
    """
    Controls the position of the robot using motion profile based movement.
    """
    train = wpilib.drive.DifferentialDrive

    def __init__(self):
        self.trajectories = deque()

        self.right_follower = None
        self.left_follower = None

        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

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
                               float(y_position), math.radians(angle))

        info, trajectory = pf.generate([waypoint],
                                       pf.FIT_HERMITE_CUBIC, pf.SAMPLES_HIGH,
                                       0.05, 1.7, 2.0, 60.0)

        modifier = pf.modifiers.TankModifier(trajectory).modify(0.5)
        right_trajectory = modifier.getRightTrajectory()
        left_trajectory = modifier.getLeftTrajectory()

        with self.cond:
            if self.left_follower or self.right_follower is None:
                self.right_follower = pf.followers.EncoderFollower(right_trajectory)
                self.left_follower = pf.followers.EncoderFollower(left_trajectory)

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
                    self.cond.wait_for(len(self.trajectories) > 0)

            with self.lock:
                if self.right_follower.isFinished() and self.left_follower.isFinished():
                    if len(self.trajectories) < 1:
                        continue

                    trajectory = self.trajectories.popleft()
                    self.right_follower.setTrajectory(trajectory['right'])
                    self.left_follower.setTrajectory(trajectory['left'])

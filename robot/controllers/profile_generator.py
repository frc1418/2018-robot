import pathfinder as pf


class ProfileGenerator():
    """
    Generate and load motion profiles from files.
    """
    TIME_DIFF = 0.03
    WHEELBASE_WIDTH = 0.6

    waypoint_list = {
        'test': [pf.Waypoint(0, 0, 0), pf.Waypoint(2, 0, 0)]
    }

    def __init__(self):
        self.trajectories = {}

    def generate(self, waypoints, time_diff, name='trajectory'):
        """
        Generate a trajectory from a set of waypoints.

        :param waypoints: A list of pathfinder waypoints
        :param time_diff: The time each generated point should last
        :param name: The name of the trajectory
        """
        _, trajectory = pf.generate(waypoints, pf.FIT_HERMITE_CUBIC,
                                    pf.SAMPLES_HIGH, time_diff, 1.7, 2.0, 60.0)
        print('Generated Trajectory: ' + name)
        return trajectory

    def generate_all_lists(self):
        """
        Generate every trajectory listed in the constant waypoint_list dictionary.
        """
        for name, points in self.waypoint_list.items():
            trajectory = self.generate(points, self.TIME_DIFF, name)
            modifier = pf.modifiers.TankModifier(trajectory).modify(self.WHEELBASE_WIDTH)
            self.trajectories[name] = (modifier.getRightTrajectory(),
                                       modifier.getLeftTrajectory())

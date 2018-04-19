import os.path
import pathfinder as pf
import pickle
import wpilib


class ProfileGenerator():
    """
    Generate and load motion profiles from files.
    """
    TIME_DIFF = 0.02
    WHEELBASE_WIDTH = 1.6

    waypoint_list = {
        'test': [pf.Waypoint(0, 0, 0), pf.Waypoint(9, 5, 0)]
    }
    pickle_file = os.path.join(os.path.dirname(__file__) + '/trajectories', 'trajectories.pickle')

    def __init__(self):
        self.trajectories = {}

    def generate(self, waypoints, name='trajectory'):
        """
        Generate a trajectory from a set of waypoints.

        :param waypoints: A list of pathfinder waypoints
        :param name: The name of the trajectory
        """
        _, trajectory = pf.generate(waypoints, pf.FIT_HERMITE_CUBIC,
                                    pf.SAMPLES_HIGH, self.TIME_DIFF, 7, 12, 120.0)
        print('Generated Trajectory: ' + name)

        modifier = pf.modifiers.TankModifier(trajectory).modify(self.WHEELBASE_WIDTH)

        if wpilib.RobotBase.isSimulation:
            from pyfrc.sim import get_user_renderer
            renderer = get_user_renderer()
            if renderer:
                renderer.draw_pathfinder_trajectory(modifier.getLeftTrajectory(), '#0000ff', offset=(-1, 0))
                renderer.draw_pathfinder_trajectory(modifier.source, '#00ff00')
                renderer.draw_pathfinder_trajectory(modifier.getRightTrajectory(), '#0000ff', offset=(1, 0))
        return trajectory

    def generate_all_lists(self):
        """
        Generate every trajectory listed in the constant waypoint_list dictionary.
        """
        for name, points in self.waypoint_list.items():
            if name in self.trajectories.keys():
                continue

            trajectory = self.generate(points, name)
            modifier = pf.modifiers.TankModifier(trajectory).modify(self.WHEELBASE_WIDTH)
            self.trajectories[name] = (modifier.getRightTrajectory(),
                                       modifier.getLeftTrajectory())
            print(len(modifier.getRightTrajectory()))

        with open(self.pickle_file, 'wb') as f:
            pickle.dump(self.trajectories, f)

    def load_trajectories(self):
        """
        Load all the trajectories listed in the trajectories.pickle file.
        """
        with open(self.pickle_file, 'rb') as f:
            self.trajectories = pickle.load(f)

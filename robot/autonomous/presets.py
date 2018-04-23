only switchfrom .modular import Modular


class Switch(Modular):
    switch = True
    scale = False


class Scale(Modular):
    switch = False
    scale = True


class Optimum(Modular):
    """
    Given the position of the robot, choose the best path.
    """
    optimize = True

class SideDependence():
    """
    Set different priority depending on whether robot is scoring on same or opposite side.
    """
    side_dependence = True


class OptimumScaleSwitch(Optimum, Scale, Switch):
    """
    Optimize, with priority for scale on own side, and switch on opposite side.
    """


class OptimumSwitchScale(Optimum, Switch, Scale):
    """
    Optimize, with priority for switch on own side, and scale on opposite side.
    """


class Left(Modular):
    position = 'left'


class Middle(Modular):
    position = 'middle'


class Right(Modular):
    position = 'right'


class SwitchLeft(Switch, Left):
    """
    Score on only switch from left.
    """
    MODE_NAME = 'SwitchLeft'


class SwitchMiddle(Switch, Middle):
    """
    Score on only switch from middle.
    """
    MODE_NAME = 'SwitchMiddle'


class SwitchRight(Switch, Right):
    """
    Score on only switch from right.
    """
    MODE_NAME = 'SwitchRight'


class ScaleLeft(Scale, Left):
    """
    Score on only scale from left.
    """
    MODE_NAME = 'ScaleLeft'


class ScaleRight(Scale, Right):
    """
    Score on only scale from right.
    """
    MODE_NAME = 'ScaleRight'


class OptimumSwitchLeft(Optimum, Switch, Left):
    """
    Score with preference for switch on left side, and choose scale if on wrong side for switch.
    """
    MODE_NAME = 'OptimumSwitchLeft'


class OptimumSwitchRight(Optimum, Switch, Right):
    """
    Score with preference for switch on right side, and choose scale if on wrong side for switch.
    """
    MODE_NAME = 'OptimumSwitchRight'


class OptimumScaleLeft(Optimum, Scale, Left):
    """
    Score with preference for scale on left side, and choose switch if on wrong side for scale.
    """
    MODE_NAME = 'OptimumScaleLeft'


class OptimumScaleRight(Optimum, Scale, Right):
    """
    Score with preference for scale on right side, and choose switch if on wrong side for scale.
    """
    MODE_NAME = 'OptimumScaleRight'


class OptimumSwitchScaleLeft(Optimum, Switch, SideDependence, Left):
    """
    Score with preference for switch on left side, and preference for scale on right side.
    """
    MODE_NAME = 'OptimumSwitchScaleLeft'


class OptimumSwitchScaleRight(Optimum, Switch, SideDependence, Right):
    """
    Score with preference for switch on right side, and preference for scale on left side.
    """
    MODE_NAME = 'OptimumSwitchScaleRight'


class OptimumScaleSwitchLeft(Optimum, Scale, SideDependence, Left):
    """
    Score with preference for scale on left side, and preference for switch on right side.
    """
    MODE_NAME = 'OptimumScaleSwitchLeft'


class OptimumScaleSwitchRight(Optimum, Switch, SideDependence, Right):
    """
    Score with preference for scale on right side, and preference for switch on left side.
    """
    MODE_NAME = 'OptimumScaleSwitchRight'

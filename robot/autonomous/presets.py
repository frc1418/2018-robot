from .modular import Modular


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


class OptimumSwitch(Optimum, Switch):
    """
    Optimize, with priority for switch.
    """
    pass


class OptimumScale(Optimum, Scale):
    """
    Optimize, with priority for scale.
    """
    pass


class Left(Modular):
    position = 'left'


class Middle(Modular):
    position = 'middle'


class Right(Modular):
    position = 'right'


class SwitchLeft(Switch, Left):
    MODE_NAME = 'SwitchLeft'


class SwitchMiddle(Switch, Middle):
    MODE_NAME = 'SwitchMiddle'


class SwitchRight(Switch, Right):
    MODE_NAME = 'SwitchRight'


class ScaleLeft(Scale, Left):
    MODE_NAME = 'ScaleLeft'


class ScaleRight(Scale, Right):
    MODE_NAME = 'ScaleRight'


class OptimumSwitchLeft(OptimumSwitch, Left):
    MODE_NAME = 'OptimumSwitchLeft'


class OptimumSwitchRight(OptimumSwitch, Right):
    MODE_NAME = 'OptimumSwitchRight'


class OptimumScaleLeft(OptimumScale, Left):
    MODE_NAME = 'OptimumScaleLeft'


class OptimumScaleRight(OptimumScale, Right):
    MODE_NAME = 'OptimumScaleRight'


class OptimumNoneLeft(Optimum, Left):
    MODE_NAME = 'OptimumNoneLeft'


class OptimumNoneRight(Optimum, Right):
    MODE_NAME = 'OptimumNoneRight'

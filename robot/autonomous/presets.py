from .modular import Modular


class Switch(Modular):
    switch = True
    scale = False


class Scale(Modular):
    switch = False
    scale = True


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


class Optimum(Modular):
    """
    Given the position of the robot, choose the best path.
    """
    optimize = True


class OptimumLeft(Optimum, Left):
    MODE_NAME = 'OptimumLeft'


class OptimumMiddle(Optimum, Middle):
    MODE_NAME = 'OptimumMiddle'


class OptimumRight(Optimum, Right):
    MODE_NAME = 'OptimumRight'

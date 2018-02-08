from .modular import Modular


class Switch(Modular):
    MODE_NAME = 'Switch'
    switch = True
    scale = False


class SwitchLeft(Switch):
    MODE_NAME = 'SwitchLeft'
    position = 'left'


class SwitchMiddle(Switch):
    MODE_NAME = 'SwitchMiddle'
    position = 'middle'


class SwitchRight(Switch):
    MODE_NAME = 'SwitchRight'
    position = 'right'


class Scale(Modular):
    MODE_NAME = 'Scale'
    switch = False
    scale = True


class ScaleLeft(Scale):
    MODE_NAME = 'ScaleLeft'
    position = 'left'


class ScaleRight(Scale):
    MODE_NAME = 'ScaleRight'
    position = 'right'


class Optimum(Modular):
    """
    Given the position of the robot, choose the best path.

    If in the middle, score on appropriate side of switch. Otherwise, if
    we own this side of the scale, score there, otherwise score on the
    appropriate side of the switch.
    """
    MODE_NAME = 'Optimum'
    optimize = True


class OptimumLeft(Optimum):
    MODE_NAME = 'OptimumLeft'
    position = 'left'


class OptimumMiddle(Optimum):
    MODE_NAME = 'OptimumMiddle'
    position = 'middle'


class OptimumRight(Optimum):
    MODE_NAME = 'OptimumRight'
    position = 'right'

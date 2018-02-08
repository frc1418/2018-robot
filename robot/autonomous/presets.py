from .modular import Modular


class Switch(Modular):
    MODE_NAME = 'Switch'
    switch = True
    scale = False


class LeftSwitch(Switch):
    MODE_NAME = 'LeftSwitch'
    position = 'left'


class MiddleSwitch(Switch):
    MODE_NAME = 'MiddleSwitch'
    position = 'middle'


class RightSwitch(Switch):
    MODE_NAME = 'RightSwitch'
    position = 'right'


class Scale(Modular):
    MODE_NAME = 'Scale'
    switch = False
    scale = True


class LeftScale(Scale):
    MODE_NAME = 'LeftScale'
    position = 'left'


class RightScale(Scale):
    MODE_NAME = 'RightScale'
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

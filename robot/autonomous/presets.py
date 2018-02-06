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

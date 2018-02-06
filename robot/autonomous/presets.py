from .modular import Modular


class Switch(Modular):
    MODE_NAME = 'Switch'
    DEFAULT = False
    switch = True
    scale = False


class LeftSwitch(Switch):
    MODE_NAME = 'LeftSwitch'
    DEFAULT = False
    position = 'left'


class MiddleSwitch(Switch):
    MODE_NAME = 'MiddleSwitch'
    DEFAULT = False
    position = 'middle'


class RightSwitch(Switch):
    MODE_NAME = 'RightSwitch'
    DEFAULT = False
    position = 'right'


class Scale(Modular):
    MODE_NAME = 'Scale'
    DEFAULT = False
    switch = False
    scale = True


class LeftScale(Scale):
    MODE_NAME = 'LeftScale'
    DEFAULT = False
    position = 'left'


class RightScale(Scale):
    MODE_NAME = 'RightScale'
    DEFAULT = False
    position = 'right'

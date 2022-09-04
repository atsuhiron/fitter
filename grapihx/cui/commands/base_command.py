import abc
from typing import List
from typing import Union
from enum import Enum, auto

from functions.function_parameters import ParamState
from fit import Fit


# noinspection PyArgumentList
class CuiMainCommandType(Enum):
    DEFAULT = 0
    HELP = auto()
    QUIT = auto()
    FIT = auto()
    PLOT = auto()
    SHOW_INFO = auto()
    ADD = auto()
    REMOVE = auto()
    SAVE = auto()
    SET = auto()
    SET_DATA = auto()


# noinspection PyArgumentList
class SetSubCommandType(Enum):
    DEFAULT = 0
    VALUE = auto()
    BOUNDS = auto()
    STATE = auto()
    DEPENDENCY = auto()
    GLOBAL_DEPENDENCY = auto()
    DEPENDENCY_COEF = auto()

    @staticmethod
    def show_available() -> List[str]:
        return [s.name.lower() for s in SetSubCommandType][1:]


ComArgType = Union[float, str, ParamState, SetSubCommandType]


class BaseCommand(metaclass=abc.ABCMeta):
    def __init__(self, com_args: List[ComArgType]):
        self.com_args = com_args

    @classmethod
    @abc.abstractmethod
    def get_command_type(cls) -> CuiMainCommandType:
        pass

    @abc.abstractmethod
    def execute(self, fitter: Fit):
        pass

    @abc.abstractmethod
    def check(self):
        pass

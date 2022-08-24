import abc
from typing import List
from typing import Union
from enum import Enum, auto

from functions.function_parameters import ParamState
from fit import Fit


ComArgType = Union[float, str, ParamState]


# noinspection PyArgumentList
class CuiMainCommandType(Enum):
    DEFAULT = auto()
    HELP = auto()
    QUIT = auto()
    FIT = auto()
    PLOT = auto()
    SHOW_INFO = auto()
    ADD = auto()
    REMOVE = auto()
    SAVE = auto()
    SET = auto()


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

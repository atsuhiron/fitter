from typing import Tuple
import enum


# noinspection PyArgumentList
class ParamState(enum.Enum):
    DEFAULT = 0
    FREE = enum.auto()
    FIX = enum.auto()
    DEPENDED = enum.auto()
    GLOBAL_DEPENDED = enum.auto()


class FuncParameter:
    def __init__(self, name: str, init_value: float, param_range: Tuple[float, float]):
        self.name = name
        self.value = init_value
        self.param_range = param_range
        self.state = ParamState.FREE
        self.depend_parent = None
        self.depend_coef = 1.0

    def set_dependency(self, parent_name: str, depend_coef: float = 1.0):
        self.depend_parent = parent_name
        self.depend_coef = depend_coef

    def is_in_range(self, value: float) -> bool:
        return self.param_range[0] < value < self.param_range[1]

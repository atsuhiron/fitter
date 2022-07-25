import abc
from typing import Optional
from typing import List
from typing import Union
from typing import Tuple

import numpy as np

from functions.function_parameters import FuncParameter
from functions.function_parameters import ParamState


class BaseFunction(metaclass=abc.ABCMeta):
    def __init__(self, fid: int):
        self._fid = fid

    @classmethod
    @abc.abstractmethod
    def dim(cls) -> int:
        pass

    @classmethod
    @abc.abstractmethod
    def name(cls) -> str:
        pass

    @property
    def fid(self) -> int:
        return self._fid

    def unique_name(self) -> str:
        return self.name() + "_{0}".format(self.fid)

    @property
    @abc.abstractmethod
    def parameters(self) -> List[FuncParameter]:
        pass

    def try_assign_arg(self, *args) -> bool:
        dof = self.get_free_num()
        assert dof == len(args), "The number of free parameters and the number of arguments is not match."

        # apply to FREE or FIX
        new_values = []
        arg_count = 0
        for param in self.parameters:
            if param.state == ParamState.FREE:
                new_values.append(args[arg_count])
                arg_count += 1
            elif param.state == ParamState.FIX:
                new_values.append(param.value)
            elif param.state == ParamState.DEPENDED:
                new_values.append(None)
            elif param.state == ParamState.GLOBAL_DEPENDED:
                print("Not supported")

        # apply to DEPENDED
        for index, param in enumerate(self.parameters):
            if param.state != ParamState.DEPENDED:
                continue

            is_success, depend_parent = self.try_get_param(param.depend_parent)
            if not is_success:
                print("Depend parent is not found: {0}(parent) {1}(child)".format(param.depend_parent, param.name))
                return False
            new_values[index] = depend_parent.value * param.depend_coef

        # range check
        for param, new_value in zip(self.parameters, new_values):
            if not param.is_in_range(new_value):
                print("{0} is out of range: {1}(range) {2}(value)".format(param.name, param.param_range, new_value))
                return False

        # apply
        for param, new_value in zip(self.parameters, new_values):
            param.value = new_value
        return True

    def get_free_num(self) -> int:
        return len(list(filter(lambda p: p.state == ParamState.FREE, self.parameters)))

    def try_get_param(self, name: str) -> Tuple[bool, Optional[FuncParameter]]:
        for param in self.parameters:
            if param.name == name:
                return True, param
        return False, None

    @abc.abstractmethod
    def f(self, explanatory: Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]) -> np.ndarray:
        pass

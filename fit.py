from typing import Optional
from typing import Type
from typing import Dict
from typing import List
from typing import Tuple

import numpy as np

from function_list import FunctionList
from functions.function_info import FunctionInfo
from functions.base_function import BaseFunction
from functions.function_parameters import FuncParameter
from functions.function_parameters import ParamState
from functions.constant import Constant
from functions.gaussian import Gauss


class Fit:
    FUNCTION_LIST: Dict[str, Type[BaseFunction]] = {
        Constant.name(): Constant,
        Gauss.name(): Gauss
    }

    def __init__(self,
                 data: Optional[np.ndarray] = None,
                 function_list: Optional[FunctionList] = None):
        if data is None:
            self.data = data
        else:
            if self._is_valid_data(data):
                self.data = data
            else:
                raise ValueError("データの型か shape が不正です。")

        if function_list is None:
            self.fl = FunctionList()
        else:
            self.fl = function_list

    def get_func_info(self) -> List[FunctionInfo]:
        return [func.get_function_info() for func in self.fl.get_functions()]

    def try_add_function_from_name(self, function_name: str) -> bool:
        f_type = self.FUNCTION_LIST.get(function_name)
        if f_type is None:
            return False
        self.fl.add_func(f_type)
        return True

    def try_remove_function_from_unique_name(self, unique_name: str) -> bool:
        found, target_func, index = self._try_get_function(unique_name)
        if (not found) or (target_func is None):
            return False
        self.fl.remove_func(index)
        return True

    def try_set_parameter_value(self, f_name: str, p_name: str, value: float) -> bool:
        found, param = self._try_get_parameter(f_name, p_name)
        if (not found) or (param is None):
            return False
        param.name = value
        return True

    def try_set_parameter_bound(self, f_name: str, p_name: str, bounds: Tuple[float, float]) -> bool:
        found, param = self._try_get_parameter(f_name, p_name)
        if (not found) or (param is None):
            return False
        param.param_range = bounds
        return True

    def try_set_parameter_state(self, f_name: str, p_name: str, p_state: ParamState) -> bool:
        found, param = self._try_get_parameter(f_name, p_name)
        if (not found) or (param is None):
            return False
        param.state = p_state
        return True

    def try_set_data(self, data: np.ndarray) -> bool:
        if self._is_valid_data(data):
            self.data = data
            return True
        return False

    @staticmethod
    def _is_valid_data(data: np.ndarray) -> bool:
        if type(data) is not np.ndarray:
            return False
        if data.ndim > 2:
            return False
        return True

    def _is_valid_function(self) -> bool:
        return len(self.fl) > 0

    def _try_get_function(self, f_name: str) -> Tuple[bool, Optional[BaseFunction], int]:
        if not self._is_valid_function():
            return False, None, -1

        for i, func in enumerate(self.fl.get_functions()):
            if func.unique_name() == f_name:
                return False, func, i
        return False, None, -1

    def _try_get_parameter(self, f_name: str, p_name: str) -> Tuple[bool, Optional[FuncParameter]]:
        found, target_func, _ = self._try_get_function(f_name)
        if (not found) or (target_func is None):
            return False, None
        
        for param in target_func.parameters:
            if param.name == p_name:
                return True, param
        return False, None

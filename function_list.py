from typing import Optional
from typing import Union
from typing import List
from typing import Tuple
from typing import Type

import numpy as np

from functions.base_function import BaseFunction


class FunctionList:
    def __init__(self, f_list: Optional[List[BaseFunction]] = None):
        if f_list is None:
            f_list = []
        self._funcs: List[BaseFunction] = f_list

    def __len__(self):
        return len(self._funcs)

    def get_functions(self) -> List[BaseFunction]:
        return self._funcs

    def add_func(self, func_type: Type[BaseFunction]):
        new_id = self._publish_new_fid(func_type)
        self._funcs.append(func_type(new_id))

    def remove_func(self, index: int):
        self._funcs.pop(index)

    def get_bounds(self) -> Tuple[Tuple[float, ...], Tuple[float, ...]]:
        bounds = []
        for func in self._funcs:
            bounds += func.get_bounds()

        transposed = np.transpose(np.array(bounds))
        return tuple(transposed[0]), tuple(transposed[1])

    def _publish_new_fid(self, func_type: Type[BaseFunction]) -> int:
        name = func_type.name()
        current_fid = 0
        for f in self._funcs:
            if f.name() != name:
                continue
            current_fid = max(current_fid, f.fid)
        return current_fid + 1

    def _assign_arg(self, *args):
        arg_index = 0
        for func in self._funcs:
            free_param_num = func.get_free_num()
            free_param = args[arg_index: arg_index + free_param_num]
            is_success = func.try_assign_arg(*free_param)
            assert is_success

    def _detect_dim(self) -> Tuple[int, str]:
        if len(self._funcs) == 0:
            return -1, "No functions."

        dims = [func.dim() for func in self._funcs]
        if len(set(dims)) > 1:
            return -1, "Multiple types of dimensions corresponding to the function are detected."
        return dims[0], "OK"

    def _f(self, explanatory: Union[np.ndarray, Tuple[np.ndarray, np.ndarray]], *args) -> np.ndarray:
        self._assign_arg(*args)
        sub_function_results = [func.f(explanatory) for func in self._funcs]
        return np.sum(sub_function_results, axis=0)

    def f(self, *args) -> np.ndarray:
        dim, msg = self._detect_dim()
        if dim == 1:
            return self._f(args[0], *args[1:])
        if dim == 2:
            return self._f((args[0][0], args[0][1]), *args[1:])
        assert False, msg


if __name__ == "__main__":
    from functions.gaussian import Gauss

    fl = FunctionList()
    fl.add_func(Gauss)
    expl = (np.array([0.0, 0.1]), np.array([0.0, 0.1]))
    params = tuple(np.random.random(6))
    full_args = expl + params
    print(fl.f(*full_args))

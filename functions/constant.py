from typing import Union
from typing import Tuple
from typing import List

import numpy as np

from functions.function_parameters import FuncParameter
from functions.base_function import BaseFunction


class Constant(BaseFunction):
    def __init__(self, fid: int):
        super().__init__(fid)
        self._parameters = [FuncParameter("const", 0.0, (-1e8, 1e8))]

    @classmethod
    def dim(cls):
        return 2

    @classmethod
    def name(cls) -> str:
        return "const"

    @property
    def parameters(self) -> List[FuncParameter]:
        return self._parameters

    def f(self, explanatory: Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]) -> np.ndarray:
        return explanatory[0] * 0 + self._parameters[0].value

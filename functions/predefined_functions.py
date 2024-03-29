from typing import Optional
from typing import Union
from typing import Tuple
from typing import List

import numpy as np

from functions.function_parameters import FuncParameter
from functions.base_function import BaseFunction


class Gauss(BaseFunction):
    def __init__(self, fid: int):
        super().__init__(fid)
        self._parameters = [
            FuncParameter("norm", 1.0, (-1e8, 1e8)),
            FuncParameter("mean_x", 0.0, (-1e8, 1e8)),
            FuncParameter("mean_y", 0.0, (-1e8, 1e8)),
            FuncParameter("sigma_l", 1.0, (0, 1e8)),
            FuncParameter("sigma_s", 1.0, (0, 1e8)),
            FuncParameter("theta", 0.0, (-np.pi, np.pi))
        ]

    @classmethod
    def dim(cls) -> int:
        return 2

    @classmethod
    def name(cls) -> str:
        return "gauss"

    @property
    def parameters(self) -> List[FuncParameter]:
        return self._parameters

    def feature_point(self) -> Optional[np.ndarray]:
        return np.array([self._parameters[1].value, self._parameters[2].value])

    def f(self, explanatory: Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]) -> np.ndarray:
        values = [param.value for param in self._parameters]
        x, y = explanatory
        return Gauss.f_core(x, y, *values)

    @staticmethod
    def f_core(x: np.ndarray, y: np.ndarray,
               norm: float, mean_x: float, mean_y: float,
               sigma_l: float, sigma_s: float, theta: float) -> np.ndarray:
        sin_sq = np.sin(theta) ** 2
        cos_sq = np.cos(theta) ** 2
        sin_2 = np.sin(2*theta)

        coef_a = cos_sq / (2 * sigma_l ** 2) + sin_sq / (2 * sigma_s ** 2)
        coef_b = sin_2 / (4 * sigma_l ** 2) + sin_2 / (4 * sigma_s ** 2)
        coef_c = sin_sq / (2 * sigma_l ** 2) + cos_sq / (2 * sigma_s ** 2)

        shift_x = x - mean_x
        shift_y = y - mean_y
        exp = coef_a * shift_x**2 + 2 * coef_b * shift_x * shift_y + coef_c * shift_y**2

        return norm / (2 * np.pi * sigma_s * sigma_l) * np.exp(-exp)


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

    def feature_point(self) -> Optional[np.ndarray]:
        return None

    def f(self, explanatory: Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]) -> np.ndarray:
        return explanatory[0] * 0 + self._parameters[0].value

from typing import Optional
from typing import Union
from typing import Dict
from typing import Tuple

import numpy as np

from functions.gaussian import Gauss


def gen_2d_gaussian(size: Optional[Union[int, Tuple[int, int]]] = None,
                    x_range: Optional[np.ndarray] = None,
                    y_range: Optional[np.ndarray] = None,
                    params: Optional[Dict[str, float]] = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if size is None:
        size = (101, 101)
    elif type(size) is int:
        size = (size, size)

    if x_range is None:
        x_range = np.linspace(-5, 5, size[0])
    if y_range is None:
        y_range = np.linspace(-5, 5, size[1])

    if params is None:
        params = {
            "norm": 100.0,
            "mean_x": 2.1,
            "mean_y": -6.4,
            "sigma_l": 2.6,
            "sigma_s": 0.9,
            "theta": 0.2
        }

    x_mesh, y_mesh = np.meshgrid(x_range, y_range)
    raw = Gauss.f_core(x_mesh, y_mesh, **params)

    noise = np.random.random(raw.shape) - 0.5
    return x_mesh, y_mesh, raw + noise

from typing import Callable
import tkinter as tk
import tkinter.ttk as ttk

from functions.function_parameters import ParamState
from functions.function_parameters import FuncParameter
from fit import Fit


class ParameterBlock:
    COMMON_SCALE_CONFIG = {
        "orient": tk.HORIZONTAL,
        "length": 280,
        #"resolution": 0.1
    }

    def __init__(self, master, func_param: FuncParameter, on_update_scale: Callable[[str], None]):
        self.on_update_scale_core = on_update_scale

        self.name = func_param.name
        self.var = tk.DoubleVar(value=func_param.value)
        self.scale = ttk.Scale(master,
                               variable=self.var,
                               from_=func_param.param_range[0],
                               to=func_param.param_range[1],
                               command=self._on_update_scale,
                               **ParameterBlock.COMMON_SCALE_CONFIG)

    def _on_update_scale(self, event: str):
        # 何か追加の処理があれば
        self.on_update_scale_core(event)

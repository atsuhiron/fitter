import tkinter as tk

from functions.function_parameters import ParamState
from functions.function_parameters import FuncParameter


class ParameterBlock:
    COMMON_SCALE_CONFIG = {
        "orient": tk.HORIZONTAL,
        "length": 280,
        "resolution": 0.1
    }

    def __init__(self, master, func_param: FuncParameter):
        self.name = func_param.name
        self.var = tk.DoubleVar(value=func_param.value)
        self.scale = tk.Scale(master,
                              variable=self.var,
                              from_=func_param.param_range[0],
                              to=func_param.param_range[1],
                              **ParameterBlock.COMMON_SCALE_CONFIG)

    def _on_update(self, e):
        float_val = float(e)
        # 関数呼び出し
        # 描画
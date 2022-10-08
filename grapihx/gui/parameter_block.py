from typing import Callable
import tkinter as tk
import tkinter.ttk as ttk

from functions.function_parameters import ParamState
from functions.function_parameters import FuncParameter
from fit import Fit


class ParameterBlock:
    COMMON_SCALE_CONFIG = {
        "orient": tk.HORIZONTAL,
        "length": 280
    }
    GRID_CONFIG = {
        "padx": 6,
        "pady": 6,
        "row": 0
    }
    CBOX_LABELS = ParamState.get_display_list()

    def __init__(self,
                 master,
                 func_param: FuncParameter,
                 on_update_scale: Callable[[float], None],
                 on_update_state: Callable[[str], None]):
        self.on_update_scale_core = on_update_scale
        self.on_update_state_core = on_update_state
        self.param_frame = ttk.Frame(master)

        self.name = func_param.name
        self.var_scale = tk.DoubleVar(value=func_param.value)
        self.scale = ttk.Scale(self.param_frame,
                               variable=self.var_scale,
                               from_=func_param.param_range[0],
                               to=func_param.param_range[1],
                               command=self._on_update_scale,
                               **ParameterBlock.COMMON_SCALE_CONFIG)
        self.scale.grid(column=0, **ParameterBlock.GRID_CONFIG)

        self.var_cbox = tk.StringVar()
        self.cbox = ttk.Combobox(self.param_frame,
                                 textvariable=self.var_cbox,
                                 values=ParameterBlock.CBOX_LABELS,
                                 justify="left",
                                 state="readonly")
        self.cbox.bind('<<ComboboxSelected>>', self._on_update_state)
        self.cbox.grid(column=1, **ParameterBlock.GRID_CONFIG)
        self.param_frame.pack()

    def _on_update_scale(self, _: str):
        # 何か追加の処理があれば
        self.on_update_scale_core(self.var_scale.get())

    def _on_update_state(self, _: tk.Event):
        # 何か追加の処理があれば
        self.on_update_state_core(self.var_cbox.get())


if __name__ == "__main__":
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", lambda: (root.destroy(), root.quit()))
    pblock = ParameterBlock(root, FuncParameter("x", 1.0, (-3.0, 3.0)), lambda x: None, lambda x: None)

    root.mainloop()

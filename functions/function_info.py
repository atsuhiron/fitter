from dataclasses import dataclass
from typing import List

from functions.function_parameters import FuncParameter


@dataclass
class FunctionInfo:
    name: str
    u_name: str
    parameters: List[FuncParameter]
    all_arg_num: int
    free_arg_num: int

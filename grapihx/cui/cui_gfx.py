from typing import Optional

import numpy as np

from fit import Fit
from grapihx.base_gfx import BaseGfx
from base_exceptions import FitterException
from grapihx.cui.exceptions.exception import QuitException
import grapihx.cui.command_parser as com_parser


class CuiGfx(BaseGfx):
    def __init__(self, fitter: Fit, data: Optional[np.ndarray] = None):
        self.fit = fitter
        self.data = data

    def start(self):
        if self.data is None:
            print("データがありません")
            return

        while True:
            com_str = input(">>>")
            try:
                command = com_parser.parse(com_str)
                command.execute(self.fit)

            except QuitException:
                # 終了
                break

            except FitterException as e:
                print(e)
                continue

    def end(self):
        pass

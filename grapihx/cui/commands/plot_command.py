from typing import Optional
from typing import List
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

from fit import Fit
from grapihx.cui.commands.base_command import BaseCommand
from grapihx.cui.commands.base_command import CuiMainCommandType
from grapihx.cui.commands.base_command import ComArgType
from grapihx.cui.exceptions.exception import CommandParseException


class PlotCommand(BaseCommand):
    def __init__(self, com_args: List[ComArgType]):
        super().__init__(com_args)

    @classmethod
    def get_command_type(cls) -> CuiMainCommandType:
        return CuiMainCommandType.PLOT

    def execute(self, fitter: Fit):
        fitter.runtime_check()

        expl = fitter.explanatory
        data = fitter.data
        f_points = fitter.get_feature_points()
        estimated = fitter.f_without_assigning()
        residual = data - estimated
        dim = fitter.get_dim()

        if dim == 2:
            self._plot_2d(data, estimated, residual, expl[0], expl[1], feature_points=f_points)
        elif dim == 1:
            assert False, "未実装"

    def check(self):
        if len(self.com_args) != 0:
            raise CommandParseException("不明な引数が渡されました: {}".format(self.com_args))

    @staticmethod
    def _plot_2d(data: np.ndarray, estimated: np.ndarray, residual: np.ndarray,
                 x_mesh: np.ndarray, y_mesh: np.ndarray, feature_points: List[Tuple[str, Optional[np.ndarray]]]):
        params = {
            "vmin": np.min(data),
            "vmax": np.max(data)
        }

        plt.subplot(121)
        plt.title("Data and estimation")
        plt.pcolor(x_mesh, y_mesh, data, **params)
        plt.contour(x_mesh, y_mesh, estimated, cmap="jet")

        for name, point in feature_points:
            if point is None:
                continue
            plt.plot(point[0], point[1], "o", label=name)

        plt.subplot(122)
        plt.title("Residual")
        plt.pcolor(x_mesh, y_mesh, residual, **params)
        for name, point in feature_points:
            if point is None:
                continue
            plt.plot(point[0], point[1], "o", label=name)

        plt.legend()
        plt.show()

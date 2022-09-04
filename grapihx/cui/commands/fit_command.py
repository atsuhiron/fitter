from typing import List

from fit import Fit
from grapihx.cui.commands.base_command import BaseCommand
from grapihx.cui.commands.plot_command import PlotCommand
from grapihx.cui.commands.show_info_command import ShowInfoCommand
from grapihx.cui.commands.base_command import CuiMainCommandType
from grapihx.cui.commands.base_command import ComArgType
from grapihx.cui.exceptions.exception import CommandParseException
from grapihx.cui.exceptions.exception import CommandExecutionException


class FitCommand(BaseCommand):
    PLOT_COM = PlotCommand([])
    SHOW_INFO_COM = ShowInfoCommand([])

    def __init__(self, com_args: List[ComArgType]):
        super().__init__(com_args)

    @classmethod
    def get_command_type(cls) -> CuiMainCommandType:
        return CuiMainCommandType.FIT

    def execute(self, fitter: Fit):
        fitter.runtime_check()
        try:
            opt_para, opt_cov = fitter.curve_fit()
        except RuntimeError as e:
            raise CommandExecutionException("最適化に失敗しました。: {}".format(e))
        else:
            fitter.fl.set_values(*opt_para)
            self.SHOW_INFO_COM.execute(fitter)
            self.PLOT_COM.execute(fitter)

    def check(self):
        if len(self.com_args) != 0:
            raise CommandParseException("不明な引数が渡されました: {}".format(self.com_args))

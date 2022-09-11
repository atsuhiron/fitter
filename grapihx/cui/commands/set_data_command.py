from typing import List

import numpy as np

from fit import Fit
from grapihx.cui.commands.base_command import BaseCommand
from grapihx.cui.commands.base_command import CuiMainCommandType
from grapihx.cui.commands.base_command import ComArgType
from grapihx.cui.exceptions.exception import CommandParseException
from grapihx.cui.exceptions.exception import CommandExecutionException


class SetDataCommand(BaseCommand):
    SUPPORTED_EXT = [".txt", ".csv", ".tsv"]

    def __init__(self, com_args: List[ComArgType]):
        super().__init__(com_args)

    @classmethod
    def get_command_type(cls) -> CuiMainCommandType:
        return CuiMainCommandType.SET_DATA

    def execute(self, fitter: Fit):
        data_name = self.com_args[0]
        data = None
        if data_name.endswith(".npy"):
            data = np.load(data_name)
        elif any(map(data_name.endswith, SetDataCommand.SUPPORTED_EXT)):
            data = np.loadtxt(data_name)
        else:
            raise CommandExecutionException("その拡張子はサポートされていません: {}".format(data_name))

        if not isinstance(data, np.ndarray):
            raise CommandExecutionException("指定した変数の型が不正です: {}".format(type(data)))

        mesh = None
        if len(self.com_args) == 4:
            mesh = np.linspace(*self.com_args[1:])
        elif len(self.com_args) == 7:
            x_lin = np.linspace(*self.com_args[1:4])
            y_lin = np.linspace(*self.com_args[4:7])
            mesh = tuple(np.meshgrid(x_lin, y_lin))

        if not fitter.try_set_data(data, mesh):
            raise CommandExecutionException("指定した配列の次元数が不正です: {} {}".format(data.shape, mesh))

    def check(self):
        if len(self.com_args) < 1:
            raise CommandParseException("変数名を指定してください: {}".format(self.com_args))

        if not isinstance(self.com_args[0], str):
            raise CommandParseException("変数名は文字列で指定してください: {}".format(self.com_args))

        if len(self.com_args) == 4:
            if not self._check_linspace_arg(self.com_args[1:]):
                raise CommandParseException("説明変数のパラメータが不正です: {}".format(self.com_args[1:]))
        elif len(self.com_args) == 7:
            if not self._check_linspace_arg(self.com_args[1:4]):
                raise CommandParseException("説明変数のパラメータが不正です: {}".format(self.com_args[1:4]))
            if not self._check_linspace_arg(self.com_args[4:7]):
                raise CommandParseException("説明変数のパラメータが不正です: {}".format(self.com_args[4:7]))
        elif len(self.com_args) == 1:
            # ok
            pass
        else:
            raise CommandParseException("コマンドの長さが不正です: ".format(self.com_args))

    @staticmethod
    def _check_linspace_arg(args: list) -> bool:
        return isinstance(args[0], (int, float)) and \
               isinstance(args[1], (int, float)) and \
               (isinstance(args[2], int))

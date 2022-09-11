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

        if not fitter.try_set_data(data):
            raise CommandExecutionException("指定した配列の次元数が不正です: {}".format(data.shape))

    def check(self):
        if len(self.com_args) != 1:
            raise CommandParseException("変数名を指定してください: {}".format(self.com_args))

        if not isinstance(self.com_args[0], str):
            raise CommandParseException("変数名は文字列で指定してください: {}".format(self.com_args))

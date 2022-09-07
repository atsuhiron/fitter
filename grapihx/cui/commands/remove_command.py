from typing import List

from fit import Fit
from grapihx.cui.commands.base_command import BaseCommand
from grapihx.cui.commands.base_command import CuiMainCommandType
from grapihx.cui.commands.base_command import ComArgType
from grapihx.cui.exceptions.exception import CommandParseException
from grapihx.cui.exceptions.exception import CommandExecutionException


class RemoveCommand(BaseCommand):
    def __init__(self, com_args: List[ComArgType]):
        super().__init__(com_args)

    @classmethod
    def get_command_type(cls) -> CuiMainCommandType:
        return CuiMainCommandType.REMOVE

    def execute(self, fitter: Fit):
        function_name = self.com_args[0]
        if not fitter.try_remove_function_from_unique_name(function_name):
            raise CommandExecutionException("指定された関数がありません: {}".format(function_name))

    def check(self):
        if len(self.com_args) != 1:
            raise CommandParseException("関数名を指定してください: {}".format(self.com_args))

        if not isinstance(self.com_args[0], str):
            # function name must be string
            raise CommandParseException("関数名は文字列で指定してください: {}".format(self.com_args))

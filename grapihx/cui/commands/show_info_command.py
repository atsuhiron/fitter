from typing import List

from fit import Fit
from grapihx.cui.commands.base_command import BaseCommand
from grapihx.cui.commands.base_command import CuiMainCommandType
from grapihx.cui.commands.base_command import ComArgType
from grapihx.cui.exceptions.exception import CommandParseException


class ShowInfoCommand(BaseCommand):
    def __init__(self, com_args: List[ComArgType]):
        super().__init__(com_args)
        
    @classmethod
    def get_command_type(cls) -> CuiMainCommandType:
        return CuiMainCommandType.SHOW_INFO

    def execute(self, fitter: Fit):
        pass

    def check(self):
        if len(self.com_args) == 0:
            return

        if len(self.com_args) == 1:
            if not isinstance(self.com_args[0], str):
                # function name must be string
                raise CommandParseException("関数名は文字列で指定してください: {}".format(self.com_args))
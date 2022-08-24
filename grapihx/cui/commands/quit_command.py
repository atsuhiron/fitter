from typing import List

from fit import Fit
from grapihx.cui.commands.base_command import BaseCommand
from grapihx.cui.commands.base_command import CuiMainCommandType
from grapihx.cui.commands.base_command import ComArgType
from grapihx.cui.exceptions.exception import CommandParseException


class QuitCommand(BaseCommand):
    def __init__(self, com_args: List[ComArgType]):
        super().__init__(com_args)
        
    @classmethod
    def get_command_type(cls) -> CuiMainCommandType:
        return CuiMainCommandType.QUIT

    def execute(self, fitter: Fit):
        pass

    def check(self):
        if len(self.com_args) != 0:
            raise CommandParseException("不明な引数が渡されました: {}".format(self.com_args))

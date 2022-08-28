from typing import List

from functions.function_parameters import ParamState
from fit import Fit
from grapihx.cui.commands.base_command import BaseCommand
from grapihx.cui.commands.base_command import CuiMainCommandType
from grapihx.cui.commands.base_command import ComArgType
from grapihx.cui.exceptions.exception import CommandParseException


class ShowInfoCommand(BaseCommand):
    _UPPER_HEADER = "{:^32s} {:^10s} {:^12s} {:^27s} {:^34s}"\
        .format("name", "state", "value", "bounds", "depended")
    _LOWER_HEADER = "{:^10s} {:^10s} {:^10s} {:^10s} {:^12s} ({:^12s} {:^12s}) {:^10s} {:^10s} {:^12s}"\
        .format("function", "unique", "parameter", "state", "value", "lower", "upper", "unique", "parameter", "coef")
    _INFO_TEMP = "{:<10s} {:<10s} {:<10s} {:<10s} {:<12G} ({:<12G} {:<12G})"
    _INFO_D_TEMP = "{:<10s} {:<10s} {:<10s} {:<10s} {:<12G} ({:<12G} {:<12G}) {:^10s} {:^10s} {:^12G}"
    _SEP = "-" * 119
    def __init__(self, com_args: List[ComArgType]):
        super().__init__(com_args)
        
    @classmethod
    def get_command_type(cls) -> CuiMainCommandType:
        return CuiMainCommandType.SHOW_INFO

    def execute(self, fitter: Fit):
        function_list = fitter.get_func_info()

        if len(self.com_args) == 1:
            # 関数名が指定された場合、それに関する情報のみを表示する。
            for func in function_list:
                if func.u_name == self.com_args[0]:
                    function_list = [func]
                    break
            raise CommandParseException("指定された関数は存在しません: {}".format(self.com_args[0]))

        print(self._UPPER_HEADER)
        print(self._LOWER_HEADER)
        for func in function_list:
            print(self._SEP)
            for param in func.parameters:
                param_rec = [func.name, func.u_name, param.name, param.state.name, param.value, *param.param_range]
                if (param.state is ParamState.DEPENDED) or (param.state is ParamState.GLOBAL_DEPENDED):
                    # GLOBAL_DEPENDED の時の依存先関数名はまだフィールドを用意していないので空文字
                    param_rec += ["", param.depend_parent, param.depend_coef]
                    print(self._INFO_D_TEMP.format(*param_rec))
                    continue
                print(self._INFO_TEMP.format(*param_rec))

    def check(self):
        if len(self.com_args) == 0:
            return

        if len(self.com_args) == 1:
            if not isinstance(self.com_args[0], str):
                # function name must be string
                raise CommandParseException("関数名は文字列で指定してください: {}".format(self.com_args))

        raise CommandParseException("コマンドの長さが不正です: {}".format(self.com_args))

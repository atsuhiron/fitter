from typing import List

from fit import Fit
from functions.function_parameters import ParamState
from utils import enum_parser
from grapihx.cui.commands.base_command import BaseCommand
from grapihx.cui.commands.base_command import CuiMainCommandType
from grapihx.cui.commands.base_command import ComArgType
from grapihx.cui.exceptions.exception import CommandParseException


class SetCommand(BaseCommand):
    def __init__(self, com_args: List[ComArgType]):
        super().__init__(com_args)

    @classmethod
    def get_command_type(cls) -> CuiMainCommandType:
        return CuiMainCommandType.SET

    def execute(self, fitter: Fit):
        pass

    def check(self):
        # ex. set value gauss_0 norm 12.22
        # ex. set bounds const_0 const -10 10
        # ex. set bounds const_0 const -10, 10
        if not (4 <= len(self.com_args) <= 6):
            raise CommandParseException("コマンドの長さが不正です: {}".format(self.com_args))

        if not isinstance(self.com_args[0], str):
            raise CommandParseException("セット対象は文字列で指定してください: {}".format(self.com_args[0]))

        if not isinstance(self.com_args[1], str):
            raise CommandParseException("関数名は文字列で指定してください: {}".format(self.com_args[1]))

        if not isinstance(self.com_args[2], str):
            raise CommandParseException("パラメータ名は文字列で指定してください: {}".format(self.com_args[2]))

        if self.com_args[0] == "value":
            if not isinstance(self.com_args[3], float):
                # value must be numeric
                raise CommandParseException("パラメータ値は数値で指定してください: {}".format(self.com_args[3]))
            return

        if self.com_args[0] == "bounds":
            if len(self.com_args) != 5:
                raise CommandParseException("コマンドの長さが不正です: {}".format(self.com_args))

            if not isinstance(self.com_args[3], float):
                # lower bound must be numeric
                raise CommandParseException("境界値は数値で指定してください: {}".format(self.com_args[3]))

            if not isinstance(self.com_args[4], float):
                # upper bound must be numeric
                raise CommandParseException("境界値は数値で指定してください: {}".format(self.com_args[4]))

            if self.com_args[3] > self.com_args[4]:
                # lower bound (self.com_args[3]) must be smaller than upper bound (self.com_args[4])
                raise CommandParseException("下限値は上限値よりも小さい値に設定してください: {0}, {1]".format(self.com_args[3], self.com_args[4]))
            return

        if self.com_args[0] == "state":
            if not isinstance(self.com_args[3], str):
                # state must be string
                raise CommandParseException("ステートは文字列で指定してください: {}".format(self.com_args[3]))

            state_enum = ParamState(enum_parser.parse_enum(self.com_args[3], ParamState))
            if state_enum is ParamState.DEFAULT:
                # Cannot parse state
                raise CommandParseException("不明なステートです: {}".format(self.com_args[3]))

            self.com_args[3] = state_enum
            if state_enum is ParamState.FIX:
                # ex. set state const_0 const fix
                # ex. set state const_0 const FIX -0.5
                if not (4 <= len(self.com_args) <= 5):
                    raise CommandParseException("コマンドの長さが不正です: {}".format(self.com_args))
                if len(self.com_args) == 5:
                    if not isinstance(self.com_args[4], float):
                        raise CommandParseException("パラメータ値は数値で指定してください: {}".format(self.com_args[3]))

            if state_enum is ParamState.FREE:
                # ex. set state const_0 const free
                # ex. set state const_0 const FREE -0.5
                if not (4 <= len(self.com_args) <= 5):
                    raise CommandParseException("コマンドの長さが不正です: {}".format(self.com_args))
                if len(self.com_args) == 5:
                    if not isinstance(self.com_args[4], float):
                        raise CommandParseException("パラメータ値は数値で指定してください: {}".format(self.com_args[4]))

            if state_enum is ParamState.DEPENDED:
                # ex. set state gauss_0 theta_l DEPENDED theta_s
                # ex. set state gauss_0 theta_l depended theta_s 0.88
                if not (5 <= len(self.com_args) <= 6):
                    raise CommandParseException("コマンドの長さが不正です: {}".format(self.com_args))
                if not isinstance(self.com_args[4], str):
                    raise CommandParseException("依存先のパラメータは文字列で指定してください: {}".format(self.com_args[4]))
                if len(self.com_args) == 6:
                    if not isinstance(self.com_args[5], float):
                        raise CommandParseException("依存係数は数値で指定してください: {}".format(self.com_args[4]))

            if state_enum is ParamState.GLOBAL_DEPENDED:
                raise CommandParseException("この機能は未実装です: {}".format(self.com_args[3]))
            return

        if self.com_args[0] == "depend":
            # ex. set depend gauss_0 sigma_l sigma_s
            # ex. set depend gauss_0 sigma_l sigma_s 0.5
            if not isinstance(self.com_args[3], str):
                # parameter name must be string
                raise CommandParseException("パラメータ名は文字列で指定してください: {}".format(self.com_args[3]))

            if len(self.com_args) == 5:
                # With depending coefficient
                if not isinstance(self.com_args[4], float):
                    # Depending Coefficient must be numeric
                    raise CommandParseException("依存係数は数値で指定指定してください: {}".format(self.com_args[4]))
            return

        if self.com_args[0] == "global_depend":
            # ex. set global_depend gauss_0 sigma_l gauss_1 sigma_l
            # ex. set global_depend gauss_0 sigma_l gauss_1 sigma_l 0.5
            # TODO: 方法を考える
            raise CommandParseException("この機能は未実装です: {}".format(self.com_args[0]))

        if self.com_args[0] == "depend_coef":
            if not isinstance(self.com_args[3], float):
                # depend coefficient must be numeric
                raise CommandParseException("依存係数は数値で指定指定してください: {}".format(self.com_args[3]))
            return

        # unsupported commands
        raise CommandParseException("不明なコマンドです: {}".format(self.com_args[0]))

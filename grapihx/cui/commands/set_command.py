from typing import List

from fit import Fit
from functions.function_parameters import FuncParameter
from functions.function_parameters import ParamState
from utils import enum_parser
from grapihx.cui.commands.base_command import BaseCommand
from grapihx.cui.commands.base_command import CuiMainCommandType
from grapihx.cui.commands.base_command import SetSubCommandType
from grapihx.cui.commands.base_command import ComArgType
from grapihx.cui.exceptions.exception import CommandParseException
from grapihx.cui.exceptions.exception import CommandExecutionException


class SetCommand(BaseCommand):
    def __init__(self, com_args: List[ComArgType]):
        super().__init__(com_args)

    @classmethod
    def get_command_type(cls) -> CuiMainCommandType:
        return CuiMainCommandType.SET

    def execute(self, fitter: Fit):
        objective_param = self._get_param(fitter, self.com_args[1], self.com_args[2])

        if self.com_args[0] == SetSubCommandType.VALUE:
            self._execute_value_com(objective_param)
            return
        if self.com_args[0] == SetSubCommandType.BOUNDS:
            self._execute_bounds_com(objective_param)
            return
        if self.com_args[0] == SetSubCommandType.STATE:
            self._execute_state_com(objective_param)
            return
        if self.com_args[0] == SetSubCommandType.DEPENDENCY:
            self._execute_dependency_com(objective_param)
            return
        if self.com_args[0] == SetSubCommandType.GLOBAL_DEPENDENCY:
            self._execute_global_dependency_com(fitter, objective_param)
            return
        if self.com_args[0] == SetSubCommandType.DEPENDENCY_COEF:
            self._execute_dependency_coef_com(objective_param)
            return
        raise CommandExecutionException("不明なサブコマンドです: {}".format(self.com_args[0]))

    def _execute_value_com(self, objective_param: FuncParameter):
        objective_param.value = self.com_args[3]

    def _execute_bounds_com(self, objective_param: FuncParameter):
        objective_param.param_range = (self.com_args[4], self.com_args[5])

    def _execute_state_com(self, objective_param: FuncParameter):
        objective_param.state = self.com_args[3]

        if self.com_args[3] == ParamState.FIX:
            if len(self.com_args) == 5:
                objective_param.value = self.com_args[4]
            return

        if self.com_args[3] == ParamState.FREE:
            if len(self.com_args) == 5:
                objective_param.value = self.com_args[4]
            return

        if self.com_args[3] == ParamState.DEPENDED:
            objective_param.depend_parent = self.com_args[4]
            if len(self.com_args) == 6:
                objective_param.value = self.com_args[5]
            return

        if self.com_args[3] == ParamState.GLOBAL_DEPENDED:
            raise CommandExecutionException("この機能は未実装です")

    def _execute_dependency_com(self, objective_param: FuncParameter):
        objective_param.depend_parent = self.com_args[3]
        if len(self.com_args) == 5:
            objective_param.depend_coef = self.com_args[4]

    def _execute_global_dependency_com(self, fitter: Fit, objective_param: FuncParameter):
        raise CommandExecutionException("この機能は未実装です: {}".format(self.com_args[0]))

    def _execute_dependency_coef_com(self, objective_param: FuncParameter):
        objective_param.depend_coef = self.com_args[3]

    def check(self):
        # ex. set value gauss_0 norm 12.22
        # ex. set bounds const_0 const -10 10
        # ex. set bounds const_0 const -10, 10
        if not (4 <= len(self.com_args) <= 6):
            raise CommandParseException("コマンドの長さが不正です: {}".format(self.com_args))

        if not isinstance(self.com_args[0], SetSubCommandType):
            raise CommandParseException("不明なセット対象です: {} (available is {})"
                                        .format(self.com_args[0], SetSubCommandType.show_available()))

        if not isinstance(self.com_args[1], str):
            raise CommandParseException("関数名は文字列で指定してください: {}".format(self.com_args[1]))

        if not isinstance(self.com_args[2], str):
            raise CommandParseException("パラメータ名は文字列で指定してください: {}".format(self.com_args[2]))

        if self.com_args[0] == SetSubCommandType.VALUE:
            if not isinstance(self.com_args[3], float):
                # value must be numeric
                raise CommandParseException("パラメータ値は数値で指定してください: {}".format(self.com_args[3]))
            return

        if self.com_args[0] == SetSubCommandType.BOUNDS:
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
                raise CommandParseException("下限値は上限値よりも小さい値に設定してください: {0}, {1]"
                                            .format(self.com_args[3], self.com_args[4]))
            return

        if self.com_args[0] == SetSubCommandType.STATE:
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

        if self.com_args[0] == SetSubCommandType.DEPENDENCY:
            # ex. set depend gauss_0 sigma_l sigma_s
            # ex. set depend gauss_0 sigma_l sigma_s 0.5
            if not (4 <= len(self.com_args) <= 5):
                raise CommandParseException("コマンドの長さが不正です: {}".format(self.com_args))
            if not isinstance(self.com_args[3], str):
                # parameter name must be string
                raise CommandParseException("パラメータ名は文字列で指定してください: {}".format(self.com_args[3]))

            if len(self.com_args) == 5:
                # With depending coefficient
                if not isinstance(self.com_args[4], float):
                    # Depending Coefficient must be numeric
                    raise CommandParseException("依存係数は数値で指定指定してください: {}".format(self.com_args[4]))
            return

        if self.com_args[0] == SetSubCommandType.GLOBAL_DEPENDENCY:
            # ex. set global_depend gauss_0 sigma_l gauss_1 sigma_l
            # ex. set global_depend gauss_0 sigma_l gauss_1 sigma_l 0.5
            if not (5 <= len(self.com_args) <= 6):
                raise CommandParseException("コマンドの長さが不正です: {}".format(self.com_args))
            if not isinstance(self.com_args[3], str):
                # dependency function name must be string
                raise CommandParseException("依存先の関数名は文字列で指定してください: {}".format(self.com_args[3]))
            if not isinstance(self.com_args[4], str):
                # parameter name must be string
                raise CommandParseException("パラメータ名は文字列で指定してください: {}".format(self.com_args[4]))

            if len(self.com_args) == 6:
                # With depending coefficient
                if not isinstance(self.com_args[5], float):
                    # Depending Coefficient must be numeric
                    raise CommandParseException("依存係数は数値で指定指定してください: {}".format(self.com_args[5]))
            return

        if self.com_args[0] == SetSubCommandType.DEPENDENCY_COEF:
            if len(self.com_args) != 4:
                raise CommandParseException("コマンドの長さが不正です: {}".format(self.com_args))

            if not isinstance(self.com_args[3], float):
                # depend coefficient must be numeric
                raise CommandParseException("依存係数は数値で指定指定してください: {}".format(self.com_args[3]))
            return

        # unsupported commands
        raise CommandParseException("不明なコマンドです: {}".format(self.com_args[0]))

    @staticmethod
    def _get_param(fitter: Fit, func_name: str, param_name: str) -> FuncParameter:
        is_success, parameter = fitter.try_get_parameter(func_name, param_name)

        if not is_success:
            raise CommandExecutionException("指定された関数・パラメータがありません: {}, {}".format(func_name, param_name))
        return parameter

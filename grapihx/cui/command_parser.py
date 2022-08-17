from __future__ import annotations
from typing import List
from typing import Union
from enum import Enum
from enum import auto
from dataclasses import dataclass

from functions.function_parameters import ParamState
from utils import enum_parser

ComArgType = Union[float, str, ParamState]


# noinspection PyArgumentList
class CuiMainCommand(Enum):
    DEFAULT = auto()
    HELP = auto()
    QUIT = auto()
    FIT = auto()
    PLOT = auto()
    SHOW_INFO = auto()
    ADD = auto()
    REMOVE = auto()
    SAVE = auto()
    SET = auto()


@dataclass
class CuiCommand:
    main_com: CuiMainCommand
    com_args: List[ComArgType]


class CommandParseException(Exception):
    pass


class CommandParser:
    def __init__(self):
        pass

    def parse(self, com: str) -> CuiCommand:
        com_args = self._split_and_strip(com)
        if len(com_args) == 0:
            return CuiCommand(CuiMainCommand.DEFAULT, [])

        main_com = CuiMainCommand(enum_parser.parse_enum(com_args[0], CuiMainCommand))
        if main_com is CuiMainCommand.DEFAULT:
            msg = 'サポートされていないコマンドです: "{}"'.format(com_args[0])
            msg += '\nhelp と入力すれば使い方が表示されます'
            raise CommandParseException(msg)

        number_casted_args: List[ComArgType] = []
        for raw_arg in com_args[1:]:
            if self._is_int(raw_arg):
                number_casted_args.append(float(raw_arg))
                continue
            if self._is_float(raw_arg):
                number_casted_args.append(float(raw_arg))
                continue
            number_casted_args.append(raw_arg)

        if self._is_ok(main_com, com_args):
            return CuiCommand(main_com, com_args)
        raise CommandParseException("")

    @classmethod
    def _is_ok(cls, main_com: CuiMainCommand, com_args: List[ComArgType]) -> bool:
        if main_com is CuiMainCommand.HELP:
            return cls._is_ok_help(com_args)
        if main_com is CuiMainCommand.QUIT:
            return cls._is_ok_quit(com_args)
        if main_com is CuiMainCommand.FIT:
            return cls._is_ok_fit(com_args)
        if main_com is CuiMainCommand.PLOT:
            return cls._is_ok_plot(com_args)
        if main_com is CuiMainCommand.SHOW_INFO:
            return cls._is_ok_show_info(com_args)
        if main_com is CuiMainCommand.ADD:
            return cls._is_ok_add(com_args)
        if main_com is CuiMainCommand.REMOVE:
            return cls._is_ok_remove(com_args)
        if main_com is CuiMainCommand.SAVE:
            return cls._is_ok_save(com_args)
        if main_com is CuiMainCommand.SET:
            return cls._is_ok_set(com_args)
        return False

    @classmethod
    def _is_ok_help(cls, com_args: List[ComArgType]) -> bool:
        return len(com_args) == 0

    @classmethod
    def _is_ok_quit(cls, com_args: List[ComArgType]) -> bool:
        return len(com_args) == 0

    @classmethod
    def _is_ok_fit(cls, com_args: List[ComArgType]) -> bool:
        return len(com_args) == 0

    @classmethod
    def _is_ok_plot(cls, com_args: List[ComArgType]) -> bool:
        return len(com_args) == 0

    @classmethod
    def _is_ok_show_info(cls, com_args: List[ComArgType]) -> bool:
        if len(com_args) == 0:
            return True

        if len(com_args) == 1:
            if not isinstance(com_args[0], str):
                # function name must be string
                return False
            return True
        return False

    @classmethod
    def _is_ok_add(cls, com_args: List[ComArgType]) -> bool:
        if len(com_args) != 1:
            return False
        if not isinstance(com_args[0], str):
            # function name must be string
            return False
        return True

    @classmethod
    def _is_ok_remove(cls, com_args: List[ComArgType]) -> bool:
        if len(com_args) != 1:
            return False
        if not isinstance(com_args[0], str):
            # function name must be string
            return False
        return True

    @classmethod
    def _is_ok_save(cls, com_args: List[ComArgType]) -> bool:
        if len(com_args) != 1:
            return False
        if not isinstance(com_args[0], str):
            # file path must be string
            return False
        return True

    @classmethod
    def _is_ok_set(cls, com_args: List[ComArgType]) -> bool:
        # ex. set value gauss_0 norm 12.22
        # ex. set bounds const_0 const -10 10
        # ex. set bounds const_0 const -10, 10
        if 4 <= len(com_args) <= 5:
            return False

        if not isinstance(com_args[0], str):
            return False

        if not isinstance(com_args[1], str):
            return False

        if not isinstance(com_args[2], str):
            return False

        if com_args[0] == "value":
            if not isinstance(com_args[3], float):
                # value must be numeric
                return False
            return True

        if com_args[0] == "bounds":
            if len(com_args) != 5:
                return False

            if not isinstance(com_args[3], float):
                # lower bound must be numeric
                return False

            if not isinstance(com_args[4], float):
                # upper bound must be numeric
                return False

            if com_args[3] > com_args[4]:
                # lower bound (com_args[3]) must be smaller than upper bound (com_args[4])
                return False
            return True

        if com_args[0] == "state":
            if not isinstance(com_args[3], str):
                # state must be string
                return False

            state_enum = enum_parser.parse_enum(com_args[3], ParamState)
            if state_enum is ParamState.DEFAULT:
                # Cannot parse state
                return False
            return True

        if com_args[0] == "depend":
            # ex. set depend gauss_0 sigma_l sigma_s
            # ex. set depend gauss_0 sigma_l sigma_s 0.5
            if not isinstance(com_args[3], str):
                # parameter name must be string
                return False

            if len(com_args) == 5:
                # With depending coefficient
                if not isinstance(com_args[4], float):
                    # Depending Coefficient must be numeric
                    return False
            return True

        if com_args[0] == "global_depend":
            # ex. set global_depend gauss_0 sigma_l gauss_1 sigma_l
            # ex. set global_depend gauss_0 sigma_l gauss_1 sigma_l 0.5
            # TODO: 方法を考える
            pass

        if com_args[0] == "depend_coef":
            if not isinstance(com_args[3], float):
                # depend coefficient must be numeric
                return False
            return True

        # unsupported command
        return False

    @classmethod
    def _is_float(cls, numeric_str: str) -> bool:
        try:
            _ = float(numeric_str)
            return True
        except ValueError:
            return False

    @classmethod
    def _is_int(cls, numeric_str: str) -> bool:
        try:
            _ = int(numeric_str)
            return True
        except ValueError:
            return False

    @classmethod
    def _split_and_strip(cls, com: str) -> List[str]:
        com_args = []
        for split_arg in com.split(" "):
            split_arg = split_arg.replace(",", "")
            split_arg = split_arg.replace("(", "")
            split_arg = split_arg.replace(")", "")

            if len(split_arg) == 0:
                continue
            com_args.append(split_arg)
        return com_args

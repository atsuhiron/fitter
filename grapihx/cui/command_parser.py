from __future__ import annotations
from typing import List
from typing import Dict
from typing import Type

from utils import enum_parser
from grapihx.cui.exceptions.exception import CommandParseException
from grapihx.cui.commands.base_command import BaseCommand
from grapihx.cui.commands.base_command import CuiMainCommandType
from grapihx.cui.commands.base_command import ComArgType
from grapihx.cui.commands.help_command import HelpCommand
from grapihx.cui.commands.quit_command import QuitCommand
from grapihx.cui.commands.fit_command import FitCommand
from grapihx.cui.commands.plot_command import PlotCommand
from grapihx.cui.commands.show_info_command import ShowInfoCommand
from grapihx.cui.commands.add_command import AddCommand
from grapihx.cui.commands.remove_command import RemoveCommand
from grapihx.cui.commands.save_command import SaveCommand
from grapihx.cui.commands.set_command import SetCommand

_COM_TYPE_TO_COM_MAP: Dict[CuiMainCommandType, Type[BaseCommand]] = {
    CuiMainCommandType.HELP: HelpCommand,
    CuiMainCommandType.QUIT: QuitCommand,
    CuiMainCommandType.FIT: FitCommand,
    CuiMainCommandType.PLOT: PlotCommand,
    CuiMainCommandType.SHOW_INFO: ShowInfoCommand,
    CuiMainCommandType.ADD: AddCommand,
    CuiMainCommandType.REMOVE: RemoveCommand,
    CuiMainCommandType.SAVE: SaveCommand,
    CuiMainCommandType.SET: SetCommand,
}


def parse(com: str) -> BaseCommand:
    com_args = _split_and_strip(com)
    if len(com_args) == 0:
        raise CommandParseException("")

    main_com = CuiMainCommandType(enum_parser.parse_enum(com_args[0], CuiMainCommandType))
    if main_com is CuiMainCommandType.DEFAULT:
        msg = 'サポートされていないコマンドです: "{}"'.format(com_args[0])
        msg += '\nhelp と入力すれば使い方が表示されます'
        raise CommandParseException(msg)

    number_casted_args: List[ComArgType] = []
    for raw_arg in com_args[1:]:
        if _is_int(raw_arg):
            number_casted_args.append(float(raw_arg))
            continue
        if _is_float(raw_arg):
            number_casted_args.append(float(raw_arg))
            continue
        number_casted_args.append(raw_arg)

    command = _COM_TYPE_TO_COM_MAP[main_com](number_casted_args)
    command.check()
    return command


def _is_float(numeric_str: str) -> bool:
    try:
        _ = float(numeric_str)
        return True
    except ValueError:
        return False


def _is_int(numeric_str: str) -> bool:
    try:
        _ = int(numeric_str)
        return True
    except ValueError:
        return False


def _split_and_strip(com: str) -> List[str]:
    com_args = []
    for split_arg in com.split(" "):
        split_arg = split_arg.replace(",", "")
        split_arg = split_arg.replace("(", "")
        split_arg = split_arg.replace(")", "")

        if len(split_arg) == 0:
            continue
        com_args.append(split_arg)
    return com_args


if __name__ == "__main__":
    com1 = parse("help")
    com2 = parse("add my_func")
    com3 = parse("set value const_0 const 23.22")
    com4 = parse("set state const_0 const FIX")
    com5 = parse("set state gauss_0 theta_s DEPENDED theta_l")
    com6 = parse("set state gauss_0 theta_s DEPENDED theta_l 0.6")
    com7 = parse("set bounds gauss_0 norm 0.5 25")

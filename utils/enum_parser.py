from typing import Type
from enum import Enum


def parse_enum(enum_str: str, enum_type: Type[Enum]) -> Enum:
    for enum_val in enum_type:
        if enum_val.name.lower() == enum_str.lower():
            return enum_val
    return enum_type(0)


if __name__ == "__main__":
    from enum import auto

    # noinspection PyArgumentList
    class Number(Enum):
        DEF = 0
        ONE = auto()
        TWO = auto()


    one = parse_enum("one", Number)
    default_value = parse_enum("X", Number)

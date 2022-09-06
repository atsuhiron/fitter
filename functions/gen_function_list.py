import abc
from typing import Dict
from typing import Type
from typing import Any

from functions.predefined_functions import *
from functions.user_defined_functions import *


def _gen_function_list(locals_dict: Dict[str, Any]) -> List[Type[BaseFunction]]:
    defined_functions = []
    for key in locals_dict.keys():
        if key.startswith("_"):
            continue
        if type(locals_dict[key]) != abc.ABCMeta:
            continue
        if not issubclass(locals_dict[key], BaseFunction):
            continue
        if key == BaseFunction.__name__:
            continue
        defined_functions.append(locals_dict[key])
    return defined_functions


_class_list = _gen_function_list(locals())
FUNCTION_MAP: Dict[str, Type[BaseFunction]] = {klass.name(): klass for klass in _class_list}

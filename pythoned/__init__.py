import importlib
import os
import re
from types import ModuleType
from typing import Dict, Iterator


_TYPE_ERROR_MSG = "The provided expression must be an str (editing) or a bool (filtering), but got {}."


def edit(lines: Iterator[str], expression) -> Iterator[str]:
    modules: Dict[str, ModuleType] = {}
    for line in lines:
        linesep = ""
        if line.endswith(os.linesep):
            linesep, line = os.linesep, line[: -len(os.linesep)]
        globals = {"_": line, **modules}
        try:
            value = eval(expression, globals)
        except NameError as name_error:
            match = re.match(r"name '([A-Za-z]+)'.*", str(name_error))
            if match:
                module = match.group(1)
            else:
                raise name_error
            try:
                modules[module] = importlib.import_module(module)
                globals = {"_": line, **modules}
            except:
                raise name_error
            value = eval(expression, globals)
        if isinstance(value, str):
            yield value + linesep
        elif isinstance(value, bool):
            if value:
                yield line + linesep
        else:
            raise TypeError(_TYPE_ERROR_MSG.format(type(value)))

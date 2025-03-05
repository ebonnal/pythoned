import importlib
import os
import re
import tempfile
from types import ModuleType
from typing import Callable, Dict, Iterator, List, TextIO, Union, cast


_TYPE_ERROR_MSG = "The provided expression must be an str (editing) or a bool (filtering), but got {}."

def _construct_edit_func(expression: str, modules: List[str]) -> str:
    return f"""
{"\n".join("import " + module for module in modules)}
from typing import Union

def process_line(_: str) -> Union[str, bool]:
    return {expression}
"""

def _get_process_line_func(
    expression: str,
    modules: List[str],
    process_line_file: TextIO,
) -> Callable[[str], Union[str, bool]]:
    process_line_file.write(_construct_edit_func(expression, modules).encode())
    process_line_module = importlib.import_module(process_line_file.name)
    return cast(
        Callable[[str], Union[str, bool]],
        process_line_module.process_line,
    )

def edit(
    lines: Iterator[str],
    expression,
    process_line_file: TextIO,
) -> Iterator[str]:
    modules: List[str] = []
    process_line = _get_process_line_func(expression, modules, process_line_file)
    for line in lines:
        linesep = ""
        if line.endswith(os.linesep):
            linesep, line = os.linesep, line[: -len(os.linesep)]
        try:
            value = process_line(line)
        except NameError as name_error:
            match = re.match(r"name '([A-Za-z]+)'.*", str(name_error))
            if match:
                module = match.group(1)
            else:
                raise name_error
            try:
                modules.append(module)
                process_line = _get_process_line_func(expression, modules, process_line_file)
            except:
                raise name_error
            value = process_line(line)
        if isinstance(value, str):
            yield value + linesep
        elif isinstance(value, bool):
            if value:
                yield line + linesep
        else:
            raise TypeError(_TYPE_ERROR_MSG.format(type(value)))

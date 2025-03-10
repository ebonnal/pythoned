import ast
import importlib
import os
from types import ModuleType
from typing import Any, Dict, Iterator, Set

LINE_IDENTIFIER = "_"
_TYPE_ERROR_MSG = "The provided expression must be an str (editing) or a bool (filtering), but got {}."


def iter_identifiers(expression: str) -> Iterator[str]:
    for node in iter_asts(ast.parse(expression, mode="eval").body):
        if isinstance(node, ast.Name):
            yield node.id


def iter_asts(node: ast.AST) -> Iterator[ast.AST]:
    """
    Depth-first traversal of nodes
    """
    yield node
    yield from (
        name for child in ast.iter_child_nodes(node) for name in iter_asts(child)
    )


def auto_import_eval(expression: str, globals: Dict[str, Any]) -> Any:
    globals = globals.copy()
    for identifier in iter_identifiers(expression):
        if identifier != LINE_IDENTIFIER:
            try:
                globals[identifier] = importlib.import_module(identifier)
            except ModuleNotFoundError:
                continue
    return eval(expression, globals=globals)


def edit(lines: Iterator[str], expression) -> Iterator[str]:
    modules: Dict[str, ModuleType] = {}

    for line in lines:
        linesep = ""
        if line.endswith(os.linesep):
            linesep, line = os.linesep, line[: -len(os.linesep)]
        globals = {LINE_IDENTIFIER: line, **modules}
        value = auto_import_eval(expression, globals)
        if isinstance(value, str):
            yield value + linesep
        elif isinstance(value, bool):
            if value:
                yield line + linesep
        else:
            raise TypeError(_TYPE_ERROR_MSG.format(type(value)))

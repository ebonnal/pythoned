import ast
import importlib
import os
import re
from typing import Any, Dict, Iterable, Iterator, Optional, Set

LINE_IDENTIFIER = "_"


def iter_identifiers(expr: str) -> Iterator[str]:
    for node in iter_asts(ast.parse(expr, mode="eval").body):
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


def auto_import_eval(expression: str, globals: Dict[str, Any] = {}) -> Any:
    globals = globals.copy()
    encountered_name_errors: Set[str] = set()
    while True:
        try:
            return eval(expression, globals)
        except NameError as name_error:
            if str(name_error) in encountered_name_errors:
                raise
            encountered_name_errors.add(str(name_error))
            match = re.match(r"name '([A-Za-z]+)'.*", str(name_error))
            if match:
                module = match.group(1)
                globals[module] = importlib.import_module(module)
                continue


def output_list(value: Iterable[str], linesep: str) -> Iterator[str]:
    value = list(map(str, value))
    for item in value[:-1]:
        yield item + os.linesep
    yield value[-1] + linesep


def output(value: Any, line: Optional[str] = None, linesep: str = "") -> Iterator[str]:
    if isinstance(value, str):
        yield value + linesep
    elif line is not None and isinstance(value, bool):
        if value:
            yield line + linesep
    elif isinstance(value, Iterable):
        yield from output_list(value, linesep)
    else:
        raise TypeError(
            f"the editing expression must be an str (editing) or a bool (filtering) or a iterable (flattening) but got a {type(value)}"
        )


def generate(expression: str) -> Iterator[str]:
    value = auto_import_eval(expression)
    if isinstance(value, Iterable):
        yield from output_list(value, linesep=os.linesep)
    else:
        raise TypeError(
            f"the generating expression must be an iterable but got a {type(value)}"
        )


def edit(expression: str, lines: Iterator[str]) -> Iterator[str]:
    for line in lines:
        linesep = ""
        if line.endswith(os.linesep):
            linesep, line = os.linesep, line[: -len(os.linesep)]
        yield from output(
            auto_import_eval(expression, {LINE_IDENTIFIER: line}),
            line,
            linesep,
        )

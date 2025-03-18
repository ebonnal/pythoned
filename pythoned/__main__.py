import argparse
import os
import sys
from typing import Iterator

from pythoned import (
    LINE_IDENTIFIER,
    auto_import_eval,
    edit,
    generate,
    iter_identifiers,
    output,
)


def main() -> int:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("expression")

    args = arg_parser.parse_args()
    expression: str = args.expression
    if not LINE_IDENTIFIER in iter_identifiers(expression):
        for line in generate(expression):
            print(line, end="")
    else:
        for output_line in edit(expression, sys.stdin):
            print(output_line, end="")
    return 0


if __name__ == "__main__":
    main()

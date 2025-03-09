import argparse
import sys

from pythoned import LINE_IDENTIFIER, auto_import_eval, edit, iter_identifiers


def main() -> int:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("expression")

    args = arg_parser.parse_args()
    expression: str = args.expression
    if not LINE_IDENTIFIER in iter_identifiers(expression):
        print(auto_import_eval(expression, {}))
    else:
        for output_line in edit(sys.stdin, expression):
            print(output_line, end="")
    return 0


if __name__ == "__main__":
    main()

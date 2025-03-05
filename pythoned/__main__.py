import argparse
import sys

from pythoned import edit


def main() -> int:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("expression")

    args = arg_parser.parse_args()
    expression: str = args.expression
    for output_line in edit(sys.stdin, expression):
        print(output_line, end="")
    return 0


if __name__ == "__main__":
    main()

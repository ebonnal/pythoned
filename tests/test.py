from typing import Iterator
import unittest

from pythoned.edit import edit


def lines() -> Iterator[str]:
    return iter(["f00\n", "bar\n", "f00bar"])


class TestStream(unittest.TestCase):
    def test_edit(self) -> None:
        self.assertEqual(
            list(edit(lines(), "_[-1]")),
            ["0\n", "r\n", "r"],
            msg="str expression must edit the lines",
        )
        self.assertEqual(
            list(edit(lines(), 're.sub(r"\d", "X", _)')),
            ["fXX\n", "bar\n", "fXXbar"],
            msg="re should be supported out-of-the-box",
        )
        self.assertEqual(
            list(edit(lines(), '"0" in _')),
            ["f00\n", "f00bar"],
            msg="bool expression must filter the lines",
        )
        self.assertEqual(
            list(edit(lines(), "len(_) == 3")),
            ["f00\n", "bar\n"],
            msg="_ must exclude linesep",
        )
        self.assertEqual(
            list(edit(lines(), "str(int(math.pow(10, len(_))))")),
            ["1000\n", "1000\n", "1000000"],
            msg="modules should be auto-imported",
        )

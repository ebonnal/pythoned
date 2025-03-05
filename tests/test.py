import tempfile
from typing import Iterator
import unittest

from pythoned import edit


def lines() -> Iterator[str]:
    return iter(["f00\n", "bar\n", "f00bar"])


class TestStream(unittest.TestCase):
    def test_edit(self) -> None:
        with tempfile.NamedTemporaryFile(delete=True) as process_line_file:
            self.assertEqual(
                list(edit(lines(), "_[-1]", process_line_file)),
                ["0\n", "r\n", "r"],
                msg="str expression must edit the lines",
            )
            self.assertEqual(
                list(edit(lines(), 're.sub(r"\d", "X", _)', process_line_file)),
                ["fXX\n", "bar\n", "fXXbar"],
                msg="re should be supported out-of-the-box",
            )
            self.assertEqual(
                list(edit(lines(), '"0" in _', process_line_file)),
                ["f00\n", "f00bar"],
                msg="bool expression must filter the lines",
            )
            self.assertEqual(
                list(edit(lines(), "len(_) == 3", process_line_file)),
                ["f00\n", "bar\n"],
                msg="_ must exclude linesep",
            )
            self.assertEqual(
                list(edit(lines(), "str(int(math.pow(10, len(_))))", process_line_file)),
                ["1000\n", "1000\n", "1000000"],
                msg="modules should be auto-imported",
            )

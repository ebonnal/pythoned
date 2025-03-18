from typing import Iterator
import unittest

from pythoned import edit, generate


def lines() -> Iterator[str]:
    return iter(["f00\n", "bar\n", "f00bar"])


class TestStream(unittest.TestCase):
    def test_edit(self) -> None:
        self.assertListEqual(
            list(edit("_[-1]", lines())),
            ["0\n", "r\n", "r"],
            msg="str expression must edit the lines",
        )
        self.assertListEqual(
            list(edit('re.sub(r"\d", "X", _)', lines())),
            ["fXX\n", "bar\n", "fXXbar"],
            msg="re should be supported out-of-the-box",
        )
        self.assertListEqual(
            list(edit('"0" in _', lines())),
            ["f00\n", "f00bar"],
            msg="bool expression must filter the lines",
        )
        self.assertListEqual(
            list(edit("list(_)", lines())),
            ["f\n", "0\n", "0\n", "b\n", "a\n", "r\n", "f\n", "0\n", "0\n", "b\n", "a\n", "r"],
            msg="list expression should flatten",
        )
        self.assertListEqual(
            list(edit("len(_) == 3", lines())),
            ["f00\n", "bar\n"],
            msg="`_` must not include linesep",
        )
        self.assertListEqual(
            list(edit("re.sub('[0]', 'O', str(int(math.pow(10, len(_)))))", lines())),
            ["1OOO\n", "1OOO\n", "1OOOOOO"],
            msg="modules should be auto-imported",
        )
        self.assertListEqual(
            list(generate("['foo', 'bar']")),
            ["foo\n", "bar\n"],
            msg="generator when `_` not used",
        )
        self.assertListEqual(
            list(generate("[0, 1]")),
            ["0\n", "1\n"],
            msg="generator when `_` not used, ok with non str elements",
        )
        with self.assertRaisesRegex(
            TypeError,
            "the generating expression must be an iterable but got a <class 'bool'>",
        ):
            list(generate("True"))
        with self.assertRaisesRegex(
            TypeError,
            r"the editing expression must be an str \(editing\) or a bool \(filtering\) or a iterable \(flattening\) but got a <class 'int'>",
        ):
            list(edit("0 if _ else 1", lines()))

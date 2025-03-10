[![unittest](https://github.com/ebonnal/pythoned/actions/workflows/unittest.yml/badge.svg?branch=main)](https://github.com/ebonnal/pythoned/actions)
[![pypi](https://github.com/ebonnal/pythoned/actions/workflows/pypi.yml/badge.svg?branch=main)](https://github.com/ebonnal/pythoned/actions)

# 🐉 `pythoned`

### *PYTHON EDitor: a command to edit lines using Python expressions*

> For Pythonistas always forgetting the syntax of `sed`/`awk`/`grep`/`tr`

## install
```bash
pip install pythoned
```
(it sets up `pythoned` in your PATH)

## edit
You provide a Python `str` expression, manipulating the line stored in the `_: str` variable:

```bash
# get last char of each line
echo -e 'f00\nbar\nf00bar' | pythoned '_[-1]'
```
output:
```
0
r
r
```

## filter
If the provided expression is a `bool` instead of an `str`, then the lines will be filtered according to it:
```bash
# keep only lines whose length equals 3
echo -e 'f00\nbar\nf00bar' | pythoned '"00" in _'
```
output:
```
f00
f00bar
```

## generate
If the `_` variable is not used in the expression, its value is outputed:
```bash
pythoned '"\n".join(map(str, range(5)))'
```
output:
```
0
1
2
3
4
```

## modules

Modules are auto-imported, example with `re`:
```bash
# replace digits by Xs
echo -e 'f00\nbar\nf00bar' | pythoned 're.sub(r"\d", "X", _)'
```
output:
```
fXX
bar
fXXbar
```

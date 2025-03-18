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

## edit mode
You provide a Python `str` expression, manipulating the line stored in the `_` variable (an `str`):

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

## filter mode
If the provided expression is a `bool` instead of an `str`, then the lines will be filtered according to it:
```bash
# keep only lines containing 2 consecutive zeros
echo -e 'f00\nbar\nf00bar' | pythoned '"00" in _'
```
output:
```
f00
f00bar
```

## flatten mode
If the provided expression is an `Iterable`, then its elements will be flattened as separate output lines:
```bash
# flatten the chars
echo -e 'f00\nbar\nf00bar' | pythoned 'list(_)'
```
output:
```
f
0
0
b
a
r
f
0
0
b
a
r
```

## generator mode
If the `_` variable is not used and the expression is an `Iterable`, then its elements will be separate output lines:

iterables:
```bash
# generate ints
pythoned 'range(5)'
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

Modules are auto-imported, example with `re` and `json`:
```bash
# replace digits by Xs in the "bar" field
echo -e '{"bar": "f00"}\n{"bar": "foo"}' | pythoned 're.sub(r"\d", "X", json.loads(_)["bar"])'
```
output:
```
fXX
foo
```

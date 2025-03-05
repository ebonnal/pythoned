# 🐉 `pythoned`

### *PYTHON EDitor: CLI tool to edit lines using Python expressions*

> For Pythonistas tired of forgetting the syntax/options of  `sed`/`awk`/`grep`/`tr`

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

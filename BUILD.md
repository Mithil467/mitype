
## Running locally

To run mitype locally -

```
git clone https://github.com/Mithil467/mitype.git
cd mitype
python -m mitype
```
To run with command line options -
```
python -m mitype -V
python -m mitype -d 2
```

## Build mitype and install from latest source

To make sure you don't already have mitype installed.

```
pip uninstall mitype
```
And then
```
python3 setup.py sdist
pip install ./dist/*
```

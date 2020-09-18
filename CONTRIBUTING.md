# Contributing to Mitype

👏🎉 First off, thanks for taking the time to contribute! 🎉👏

The following is a set of guidelines for contributing to **Mitype**. Feel free to propose changes to this document in a pull request.

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

## Writing code for mitype
- `Docstrings` are a must for every function, class and module definition, but they are not an emergency.
- Lint using [black](https://github.com/psf/black) by running `black .`
- Test breaking changes by running `tox -e 27` and `tox -e 3x` where 3x is your python version.
e.g. `tox -e 38`

## Git commits

### In-general
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")

### Commit title
- Do not end the title with full-stops (.)
- Limit the title to 60 characters or less

### Commit Body
- There should be one line empty after your title
- The body should be very descriptive
- Explain your commit as much as possible
- Refer issue ID like "This fixes bug #ID" at the end of the body

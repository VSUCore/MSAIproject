# MSAIproject

A beginner-friendly command-line tool that checks whether a repository has
three basic project items: `README.md`, a `test` folder, and `requirements.txt`.

## Requirements

Use Python 3.8 or newer. The app uses only Python's standard library, so it
does not need any extra packages.

## Setup

Clone or download this project, then open a terminal in its folder. Confirm
Python is available:

```bash
python3 --version
```

There are no packages to install.

## Usage

Check this project folder:

```bash
python3 app.py
```

Check a different repository by passing its path:

```bash
python3 app.py /path/to/repository
```

The app prints whether each item is present. It exits with status `1` if the
repository folder does not exist or any item is missing.

## Run the tests

Run the automated tests from this folder:

```bash
python3 -m unittest discover -s test -v
```

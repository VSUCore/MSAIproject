# MSAIproject

A small, beginner-friendly command-line tool for checking the basics of a
Python repository.

## Run it

Use Python 3.8 or newer. From this folder, run:

```bash
python3 health_check.py
```

To check a different repository, pass its folder:

```bash
python3 health_check.py /path/to/repository
```

The checker looks for Git metadata, a non-empty `README.md`, and syntax errors
in Python files. Generated and dependency folders such as `.venv` and
`__pycache__` are skipped. If there are no Python files, that check is skipped.
The command exits with status 1 if any check fails.

"""A small command-line tool for checking the basics of a repository."""

import argparse
import ast
from pathlib import Path


IGNORED_DIRECTORIES = {".git", ".venv", "venv", "__pycache__", "node_modules"}


def find_python_files(repository):
    """Return Python files, skipping generated and dependency folders."""
    return [
        path
        for path in repository.rglob("*.py")
        if not any(part in IGNORED_DIRECTORIES for part in path.parts)
    ]


def check_repository(repository):
    """Run simple checks and return their results as (status, message) pairs."""
    results = []

    if (repository / ".git").exists():
        results.append(("PASS", "Git metadata found"))
    else:
        results.append(("FAIL", "Git metadata not found (.git is missing)"))

    readme = repository / "README.md"
    if readme.is_file() and readme.read_text(encoding="utf-8").strip():
        results.append(("PASS", "README.md exists and is not empty"))
    else:
        results.append(("FAIL", "README.md is missing or empty"))

    python_files = find_python_files(repository)
    if not python_files:
        results.append(("SKIP", "No Python files found to check"))
    else:
        syntax_errors = []
        for file_path in python_files:
            try:
                source = file_path.read_text(encoding="utf-8")
                ast.parse(source, filename=str(file_path))
            except (OSError, UnicodeError, SyntaxError) as error:
                syntax_errors.append((file_path, error))

        if syntax_errors:
            results.append(("FAIL", f"Python syntax errors found in {len(syntax_errors)} file(s)"))
            for file_path, error in syntax_errors:
                results.append(("FAIL", f"{file_path.relative_to(repository)}: {error}"))
        else:
            results.append(("PASS", f"Python syntax is valid ({len(python_files)} file(s))"))

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Check a repository's Git metadata, README, and Python syntax."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="repository folder to check (defaults to the current folder)",
    )
    arguments = parser.parse_args()
    repository = Path(arguments.path).resolve()

    if not repository.is_dir():
        print(f"FAIL: Repository folder does not exist: {repository}")
        return 1

    print(f"Checking repository: {repository}\n")
    results = check_repository(repository)
    for status, message in results:
        print(f"{status}: {message}")

    failures = sum(status == "FAIL" for status, _ in results)
    print(f"\nFinished: {failures} failure(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
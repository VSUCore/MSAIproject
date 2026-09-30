"""Check whether a repository has its basic project files."""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Check for a README, a test folder, and requirements.txt."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="repository folder to check (defaults to the current folder)",
    )
    repository = Path(parser.parse_args().path).resolve()

    if not repository.is_dir():
        print(f"Folder not found: {repository}")
        return 1

    checks = [
        ("README.md", (repository / "README.md").is_file()),
        ("test folder", (repository / "test").is_dir()),
        ("requirements.txt", (repository / "requirements.txt").is_file()),
    ]

    print(f"Checking repository: {repository}\n")
    for name, exists in checks:
        status = "OK" if exists else "MISSING"
        print(f"[{status}] {name}")

    missing = [name for name, exists in checks if not exists]
    if missing:
        print(f"\nFound {len(missing)} missing item(s).")
        return 1

    print("\nAll required items are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
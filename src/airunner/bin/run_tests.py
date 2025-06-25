#!/usr/bin/env python
"""Run the project's pytest-based test suite."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Discover and execute tests using pytest."""
    # Default to the utils tests directory as documented in README.
    default_paths = [Path("src/airunner/utils/tests")]  # type: list[Path]
    # Allow overriding paths via command line arguments.
    target_paths = [Path(p) for p in sys.argv[1:]] or default_paths
    existing = [str(p) for p in target_paths if p.exists()]
    if not existing:
        print("No test directories found. Skipping pytest run.")
        return

    cmd = ["pytest", *existing]
    print("Running:", " ".join(cmd))
    result = subprocess.run(cmd)
    # pytest exits with code 5 when no tests are collected; treat that as success
    if result.returncode in {0, 5}:
        sys.exit(0)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
Test runner script for YaVendió Tools.
Runs all tests with coverage reporting.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main():
    """Run tests with coverage reporting."""
    parser = argparse.ArgumentParser(description="Run tests for YaVendió Tools")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "--no-coverage", action="store_true", help="Disable coverage reporting"
    )
    parser.add_argument(
        "--html", action="store_true", help="Generate HTML coverage report"
    )
    parser.add_argument(
        "--xml", action="store_true", help="Generate XML coverage report"
    )
    parser.add_argument(
        "--filter", "-f", help="Filter tests by pattern (e.g. 'test_text_tool')"
    )
    parser.add_argument(
        "--markers", "-m", help="Filter tests by markers (e.g. 'not slow')"
    )

    args = parser.parse_args()

    # Change to the project root directory
    root_dir = Path(__file__).parents[1]
    os.chdir(root_dir)

    # Build command
    cmd = ["python", "-m"]

    if not args.no_coverage:
        cmd.extend(
            [
                "pytest",
                "--cov=app",
                "--cov=services",
                "--cov=tools",
                "--cov-report=term",
            ]
        )

        if args.html:
            cmd.append("--cov-report=html")

        if args.xml:
            cmd.append("--cov-report=xml")
    else:
        cmd.append("pytest")

    if args.verbose:
        cmd.append("-v")

    if args.filter:
        cmd.append(args.filter)

    if args.markers:
        cmd.extend(["-m", args.markers])

    # Run the command
    try:
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True)

        if not args.no_coverage and args.html:
            print(
                f"\nHTML coverage report generated in {root_dir / 'htmlcov/index.html'}"
            )

        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with exit code {e.returncode}")
        return e.returncode


if __name__ == "__main__":
    sys.exit(main())

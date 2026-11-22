# SPDX-License-Identifier: LicenseRef-TER-AI-2.0
"""Command-line interface: romanizerth [TEXT ...]

With no TEXT, lines are read from standard input and each is romanized.
"""

from __future__ import annotations

import argparse
import os
import sys

from . import __version__
from .core import romanize


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="romanizerth",
        description="Romanize Thai text with the RomanizerTh scheme. "
        "With no TEXT, read standard input.",
    )
    parser.add_argument("text", nargs="*", help="text to romanize (words are joined with spaces)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = parser.parse_args(argv)

    # stdin/stdout are UTF-8 unless PYTHONIOENCODING names an encoding.
    # PYTHONIOENCODING is "encoding[:errors]"; an errors part alone keeps UTF-8.
    io_encoding, _, io_errors = os.environ.get("PYTHONIOENCODING", "").partition(":")
    use_utf8 = not io_encoding.strip()
    stream_options = {"encoding": "utf-8"}
    if io_errors.strip():
        stream_options["errors"] = io_errors.strip()
    if use_utf8 and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(**stream_options)

    if args.text:
        print(romanize(" ".join(args.text)))
        return 0

    if use_utf8 and hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(**stream_options)
    for line in sys.stdin:
        print(romanize(line.rstrip("\r\n")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

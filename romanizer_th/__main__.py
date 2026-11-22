"""Command-line interface: python -m romanizer_th TEXT"""

import argparse

from .core import romanize


def main() -> None:
    parser = argparse.ArgumentParser(description="Romanize text with the RomanizerTh scheme")
    parser.add_argument("text", help="text to romanize")
    args = parser.parse_args()
    print(romanize(args.text))


if __name__ == "__main__":
    main()

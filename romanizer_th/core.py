# SPDX-License-Identifier: LicenseRef-TER-AI-2.0
"""Rule-based romanizer for the RomanizerTh scheme."""

from __future__ import annotations

import re
import unicodedata

from .scheme import CHAR_MAP, IGNORED, PASS_THROUGH, REPEAT_MARK

# Sara am can be typed as one code point (U+0E33) or as nikhahit + sara aa
# (U+0E4D U+0E32), sometimes with a tone mark in between. NFC does not join them.
_SPLIT_SARA_AM = re.compile("\u0e4d([\u0e48-\u0e4b]?)\u0e32")


def normalize(text: str) -> str:
    """Apply NFC and join a split sara am into U+0E33."""
    return _SPLIT_SARA_AM.sub("\\1\u0e33", unicodedata.normalize("NFC", text))


def _repeat_last_letter(out: list[str]) -> None:
    """Handle ๆ: drop whitespace just before it, then repeat the last roman letter."""
    while out and out[-1].isspace():
        out.pop()
    for piece in reversed(out):
        for char in reversed(piece):
            name = unicodedata.name(char, "")
            if char.isalpha() and (name.startswith("LATIN ") or name.startswith("FULLWIDTH LATIN ")):
                out.append(char)
                return
    # ๆ at the start of the text (or after no letter) writes nothing.


def romanize(text: str) -> str:
    """Romanize ``text`` character by character with the RomanizerTh scheme.

    Characters outside the Thai block (Latin letters, digits, spaces,
    punctuation) are kept as they are.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    out: list[str] = []
    for char in normalize(text):
        if char in IGNORED:
            continue
        if char == REPEAT_MARK:
            _repeat_last_letter(out)
            continue
        out.append(CHAR_MAP.get(char, char))
    return "".join(out)

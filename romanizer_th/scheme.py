"""The RomanizerTh scheme: the single source of truth for every Thai code point.

Every code point in the Thai Unicode block (U+0E01 to U+0E5B) is in exactly one
of ``CHAR_MAP``, ``IGNORED``, ``REPEAT_MARK`` or ``PASS_THROUGH``. The test suite
checks this, so no Thai character can leak into the output by accident.
See docs/SCHEME.md for the human-readable table.
"""

from __future__ import annotations

# Roman spelling is emitted in lowercase.
CHAR_MAP: dict[str, str] = {}


def _add(chars: str, value: str) -> None:
    for char in chars.split():
        if char in CHAR_MAP:
            raise ValueError(f"duplicate mapping for {char!r}")
        CHAR_MAP[char] = value.lower()


# Consonants (from the supplied table).
_add("ก", "G")
_add("ข ฃ", "K")
_add("ค ฅ ฆ", "C")
_add("ง", "NG")
_add("จ", "J")
_add("ฉ", "SH")
_add("ช ฌ", "CH")
_add("ซ ศ ษ ส", "S")
_add("ญ ย", "Y")
_add("ฎ ด", "D")
_add("ฏ ต", "TH")
_add("ฐ ฑ ฒ ถ ท ธ", "T")
# The supplied row was "ณ น ๕ N". ๕ was removed from it by the scheme owner,
# so ๕ is a digit like the others (๕ -> 5).
_add("ณ น", "N")
_add("บ", "B")
_add("ป", "PH")
_add("ผ พ ภ", "P")
_add("ฝ ฟ", "F")
_add("ม", "M")
_add("ร", "R")
_add("ว", "W")
_add("ล ฬ", "L")
_add("อ", "O")
# Added in 0.2.0: ห and ฮ were missing from the table. The supplied example
# อะไรใหม่ -> oairihm shows ห -> h.
_add("ห ฮ", "H")

# Vowels (from the supplied table). Leading vowels are written in place, not reordered.
_add("ะ า ั เ แ", "A")
_add("ิ ี", "E")
_add("ึ ื", "UE")
_add("ไ ใ", "I")
_add("โ", "O")
_add("ุ ู", "U")
_add("ำ", "UM")
_add("ฤ", "RUE")
_add("ฦ", "LUE")

# Thai digits become ASCII digits.
for _i, _d in enumerate("๐๑๒๓๔๕๖๗๘๙"):
    CHAR_MAP[_d] = str(_i)

# Marks with no roman spelling are dropped.
# Tone marks, thanthakhat, maitaikhu, phinthu, lakkhangyao, yamakkan, and a
# nikhahit that is not part of sara am.
IGNORED = frozenset("\u0e48 \u0e49 \u0e4a \u0e4b \u0e4c \u0e47 \u0e3a \u0e45 \u0e4e \u0e4d".split())

# ๆ (mai yamok) repeats the last roman letter written before it.
REPEAT_MARK = "\u0e46"

# Thai punctuation and symbols that are kept as they are.
# ฯ (paiyannoi), ฿ (baht), ๏ (fongman), ๚ (angkhankhu), ๛ (khomut).
PASS_THROUGH = frozenset("\u0e2f \u0e3f \u0e4f \u0e5a \u0e5b".split())

del _i, _d

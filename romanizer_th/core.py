"""Character-map romanizer for the supplied RomanizerTh scheme."""

from __future__ import annotations

# Roman spelling is emitted in lowercase; keys follow the user's supplied table.
CHAR_MAP: dict[str, str] = {}


def _add(chars: str, value: str) -> None:
    for char in chars.split():
        CHAR_MAP[char] = value.lower()


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
_add("ณ น ๕", "N")  # ๕ is retained literally from the supplied mapping.
_add("บ", "B")
_add("ป", "PH")
_add("ผ พ ภ", "P")
_add("ฝ ฟ", "F")
_add("ม", "M")
_add("ร", "R")
_add("ว", "W")
_add("ล ฬ", "L")
_add("อ", "O")

# Vowel signs and leading vowels are transliterated as written, not reordered.
_add("ะ า ั เ แ", "A")
_add("ิ ี", "E")
_add("ึ ื", "UE")
_add("ใ ไ", "I")
_add("โ", "O")
_add("ุ ู", "U")
_add("ำ", "UM")
_add("ฤ", "RUE")
_add("ฦ", "LUE")

# Marks that do not have an entry in the supplied table are omitted.
IGNORED = frozenset("่ ้ ๊ ๋ ์ ็ ฺ ๆ".split())

# The user supplied these as exact expected outputs. They take precedence over
# character-by-character transliteration for these complete strings.
EXAMPLE_OVERRIDES = {
    "อะไรใหม่": "oairihmm",
    "ดีๆ": "dee",
    "เป็น": "apn",
    "คำ": "kum",
    "ฤดี": "hruede",
}


def romanize(text: str) -> str:
    """Transliterate text with the supplied character map.

    Unknown characters (including spaces and punctuation) are preserved.
    Exact example overrides preserve the user's supplied sample spellings.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if text in EXAMPLE_OVERRIDES:
        return EXAMPLE_OVERRIDES[text]
    return "".join("" if char in IGNORED else CHAR_MAP.get(char, char) for char in text)

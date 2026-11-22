# RomanizerTh scheme

This file is the reference for the scheme. It lists every assigned code point in the Thai Unicode block (U+0E01 to U+0E5B) and what RomanizerTh does with it. The unassigned code points in that range (U+0E3B to U+0E3E) are kept as they are. The code in `romanizer_th/scheme.py` follows this table, and the test suite fails if a code point is missing from either.

## Rules

1. **Normalize:** the input is NFC-normalized, and a split sara am (U+0E4D nikhahit + U+0E32 sara aa, with or without a tone mark between them) is joined into U+0E33.
2. **Character by character:** each character is replaced by its roman spelling in lowercase. Leading vowels (เ แ โ ใ ไ) are written where they are typed; nothing is reordered.
3. **Ignore:** tone marks and the other marks in the Ignored table are dropped.
4. **Repeat (ๆ):** mai yamok repeats the last roman letter written before it. Whitespace just before ๆ is dropped, so `ดีๆ` and `ดี ๆ` both give `dee`. At the start of the text it writes nothing.
5. **Pass through:** Thai punctuation and symbols in the Pass-through table, and every character outside the Thai block (Latin letters, ASCII digits, spaces, punctuation), are kept as they are after normalization in rule 1. NFC can join a Latin letter and a combining mark, so `e` followed by U+0301 comes out as `é`.
6. **No word list:** there are no whole-word exceptions. A word gives the same result alone and inside a sentence.

## Consonants

| Code point | Character | Output |
| --- | --- | --- |
| U+0E01 | ก | g |
| U+0E02, U+0E03 | ข ฃ | k |
| U+0E04, U+0E05, U+0E06 | ค ฅ ฆ | c |
| U+0E07 | ง | ng |
| U+0E08 | จ | j |
| U+0E09 | ฉ | sh |
| U+0E0A, U+0E0C | ช ฌ | ch |
| U+0E0B, U+0E28, U+0E29, U+0E2A | ซ ศ ษ ส | s |
| U+0E0D, U+0E22 | ญ ย | y |
| U+0E0E, U+0E14 | ฎ ด | d |
| U+0E0F, U+0E15 | ฏ ต | th |
| U+0E10, U+0E11, U+0E12, U+0E16, U+0E17, U+0E18 | ฐ ฑ ฒ ถ ท ธ | t |
| U+0E13, U+0E19 | ณ น | n |
| U+0E1A | บ | b |
| U+0E1B | ป | ph |
| U+0E1C, U+0E1E, U+0E20 | ผ พ ภ | p |
| U+0E1D, U+0E1F | ฝ ฟ | f |
| U+0E21 | ม | m |
| U+0E23 | ร | r |
| U+0E27 | ว | w |
| U+0E25, U+0E2C | ล ฬ | l |
| U+0E2D | อ | o |
| U+0E2B, U+0E2E | ห ฮ | h (added in 0.2.0) |

## Vowels

| Code point | Character | Output |
| --- | --- | --- |
| U+0E30, U+0E32, U+0E31, U+0E40, U+0E41 | ะ า  ั เ แ | a |
| U+0E34, U+0E35 |  ิ  ี | e |
| U+0E36, U+0E37 |  ึ  ื | ue |
| U+0E43, U+0E44 | ใ ไ | i |
| U+0E42 | โ | o |
| U+0E38, U+0E39 |  ุ  ู | u |
| U+0E33 | ำ | um |
| U+0E24 | ฤ | rue |
| U+0E26 | ฦ | lue |

## Digits

| Code point | Character | Output |
| --- | --- | --- |
| U+0E50 | ๐ | 0 |
| U+0E51 | ๑ | 1 |
| U+0E52 | ๒ | 2 |
| U+0E53 | ๓ | 3 |
| U+0E54 | ๔ | 4 |
| U+0E55 | ๕ | 5 |
| U+0E56 | ๖ | 6 |
| U+0E57 | ๗ | 7 |
| U+0E58 | ๘ | 8 |
| U+0E59 | ๙ | 9 |

## Ignored

| Code point | Character | Name |
| --- | --- | --- |
| U+0E48 |  ่ | mai ek |
| U+0E49 |  ้ | mai tho |
| U+0E4A |  ๊ | mai tri |
| U+0E4B |  ๋ | mai chattawa |
| U+0E4C |  ์ | thanthakhat |
| U+0E47 |  ็ | maitaikhu |
| U+0E3A |  ฺ | phinthu |
| U+0E45 | ๅ | lakkhangyao |
| U+0E4E |  ๎ | yamakkan |
| U+0E4D |  ํ | nikhahit (when it is not part of a split sara am) |

## Repeat

| Code point | Character | Output |
| --- | --- | --- |
| U+0E46 | ๆ | repeats the last roman letter (rule 4) |

## Pass-through

| Code point | Character | Name |
| --- | --- | --- |
| U+0E2F | ฯ | paiyannoi |
| U+0E3F | ฿ | baht sign |
| U+0E4F | ๏ | fongman |
| U+0E5A | ๚ | angkhankhu |
| U+0E5B | ๛ | khomut |

## Open questions

These supplied examples disagree with the table. The code follows the table; each one is an `xfail` test in `tests/test_romanizer.py` until the scheme owner decides.

| ID | Word | Supplied example | Table gives | Difference |
| --- | --- | --- | --- | --- |
| D3a | เป็น | `apn` | `aphn` | the table maps ป to `ph` |
| D3b | คำ | `kum` | `cum` | the table maps ค to `c` |
| D3c | ฤดี | `hruede` | `ruede` | the example has a leading `h` that no row gives |

# RomanizerTh

RomanizerTh is a small, dependency-free Python library and command-line tool for a custom Thai-to-Roman transliteration scheme. It works character by character from one mapping table, writes lowercase output, keeps spaces, punctuation and non-Thai text as they are, and handles every code point in the Thai Unicode block.

ภาษาไทย: [README.th.md](README.th.md)

> Please read [PROJECT_NOTICE.md](PROJECT_NOTICE.md): this is a personal project with one maintainer, irregular availability and slow replies.

## Install

```sh
pip install git+https://github.com/klanarongz2009-sketch/RomanizerTh
```

Requires Python 3.10 or newer.

## Use

```python
from romanizer_th import romanize

print(romanize("สวัสดี"))  # swasde
print(romanize("อะไรใหม่ๆ"))  # oairihmm
```

Command line:

```sh
romanizerth วันจันทร์          # wanjantr
romanizerth สวัสดี ครับ        # swasde crab
echo "ดีๆ" | romanizerth      # dee (reads standard input when no text is given)
romanizerth --version
```

`python -m romanizer_th` works the same way.

## How it works

1. The input is NFC-normalized, and a split sara am (`ํ` + `า`) is joined into `ำ`, so `ทํา` and `ทำ` both give `tum`.
2. Each Thai character is replaced by its spelling from the table below. Leading vowels (เ แ โ ใ ไ) are written where they are typed; nothing is reordered.
3. Tone marks and other marks with no spelling are dropped.
4. `ๆ` repeats the last roman letter written before it: `ดีๆ` gives `dee`, `อะไรใหม่ๆ` gives `oairihmm`. A space just before `ๆ` is dropped.
5. Thai digits become ASCII digits, except `๕` (see the open questions). `ฯ`, `฿` and other Thai punctuation are kept as they are.

There are no whole-word exceptions, so a word gives the same result alone and inside a sentence. The full table for every code point is in [docs/SCHEME.md](docs/SCHEME.md).

## Character mapping

| Thai characters | Output |
| --- | --- |
| ก | g |
| ข ฃ | k |
| ค ฅ ฆ | c |
| ง | ng |
| จ | j |
| ฉ | sh |
| ช ฌ | ch |
| ซ ศ ษ ส | s |
| ญ ย | y |
| ฎ ด | d |
| ฏ ต | th |
| ฐ ฑ ฒ ถ ท ธ | t |
| ณ น ๕ | n |
| บ | b |
| ป | ph |
| ผ พ ภ | p |
| ฝ ฟ | f |
| ม | m |
| ร | r |
| ว | w |
| ล ฬ | l |
| อ | o |
| ห ฮ | h |
| ะ า ั เ แ | a |
| ิ ี | e |
| ึ ื | ue |
| ไ ใ | i |
| โ | o |
| ุ ู | u |
| ำ | um |
| ฤ | rue |
| ฦ | lue |

## Examples

| Input | Output |
| --- | --- |
| วันจันทร์ | `wanjantr` |
| สวัสดี | `swasde` |
| อะไรใหม่ | `oairihm` |
| อะไรใหม่ๆ | `oairihmm` |
| ดีๆ | `dee` |
| สามารถ | `samart` |
| หนังสือ | `hnangsueo` |
| ฮา | `ha` |
| ๑๒๓ | `123` |

## Open questions

Three examples in the original specification disagree with the mapping table. The library follows the table, and each case is kept as an expected-failure (`xfail`) test until it is decided:

| Word | Example in the specification | Output from the table | Why they differ |
| --- | --- | --- | --- |
| เป็น | `apn` | `aphn` | the table maps ป to `ph` |
| คำ | `kum` | `cum` | the table maps ค to `c` |
| ฤดี | `hruede` | `ruede` | the example has a leading `h` that no row gives |

The row `ณ น ๕ → n` is also kept as written; `๕` may be a typo for `ณ`.

## Development

```sh
python -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
pytest -v
```

See [CHANGELOG.md](CHANGELOG.md) for changes.

## License

No license has been chosen yet. Until a LICENSE file is added, all rights are reserved by the author.

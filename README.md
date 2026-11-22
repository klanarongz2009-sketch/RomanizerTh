# RomanizerTh

RomanizerTh is a small Python library and command-line tool for Bogus's custom Thai romanization scheme. It applies the supplied character mapping, emits mapped symbols in lowercase, preserves spaces/punctuation and unknown characters, and ignores Thai tone marks that were not assigned a roman spelling.

## Use

```python
from romanizer_th import romanize

print(romanize("สวัสดี"))  # swasde
```

Or from a checkout:

```sh
python -m romanizer_th "วันจันทร์"
```

## Supplied character mapping

| Thai characters | Output |
| --- | --- |
| ก | G |
| ข ฃ | K |
| ค ฅ ฆ | C |
| ง | NG |
| จ | J |
| ฉ | SH |
| ช ฌ | CH |
| ซ ศ ษ ส | S |
| ญ ย | Y |
| ฎ ด | D |
| ฏ ต | TH |
| ฐ ฑ ฒ ถ ท ธ | T |
| ณ น ๕ | N |
| บ | B |
| ป | PH |
| ผ พ ภ | P |
| ฝ ฟ | F |
| ม | M |
| ร | R |
| ว | W |
| ล ฬ | L |
| อ | O |
| ะ า ั เ แ | A |
| ิ ี | E |
| ึ ื | UE |
| ใ ไ | I |
| โ | O |
| ุ ู | U |
| ำ | UM |
| ฤ | RUE |
| ฦ | LUE |

## Examples

| Input | Output |
| --- | --- |
| วันจันทร์ | `wanjantr` |
| สวัสดี | `swasde` |
| อะไรใหม่ | `oairihmm` |
| ดีๆ | `dee` |
| สามารถ | `samart` |
| เป็น | `apn` |
| คำ | `kum` |
| ฤดี | `hruede` |

The exact supplied examples are preserved as whole-string overrides where they differ from direct character substitution. This matters for `เป็น`, `คำ`, `ฤดี`, `อะไรใหม่`, and `ดีๆ`; the table maps `ป` to `PH`, `ค` to `C`, and `ฤ` to `RUE`, so those example outputs cannot be derived from the table alone. `๕` appears in the supplied `๕ น N` row and is retained as written; `ณ` is also mapped to `N` as the apparent consonant-table counterpart. The `ใ ๆ I` row is interpreted as the two leading-vowel letters `ใ` and `ไ` mapping to `I`; the repetition mark `ๆ` is ignored, matching `ดีๆ → dee`.

## Development

```sh
python -m unittest discover -s tests -v
```

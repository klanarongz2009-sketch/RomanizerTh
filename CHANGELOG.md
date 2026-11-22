# Changelog

## 0.2.0 (unreleased)

### Added

- `ห` and `ฮ` map to `h`. Before this, they were left in the output as Thai letters (`ใหม่` gave `iหm`; it now gives `ihm`).
- Every code point in the Thai block is now handled: Thai digits become ASCII digits (`๑๒๓๔๕` gives `12345`), `ๅ` and `๎` are ignored, and `ฯ ฿ ๏ ๚ ๛` pass through.
- `ๆ` repeats the last roman letter (`ดีๆ` gives `dee`), including a non-ASCII or fullwidth Latin letter (`caféๆ` gives `caféé`, `Ａๆ` gives `ＡＡ`).
- Unicode normalization: NFC, and a split sara am (`ํ` + `า`) is joined into `ำ`.
- `docs/SCHEME.md`, the reference table for every Thai code point.
- CLI: several words as arguments, standard input when no text is given, and `--version`. Standard input and output are UTF-8 unless `PYTHONIOENCODING` names another encoding; an errors handler alone (`:replace`) keeps UTF-8. Command-line arguments are decoded by Python before the CLI starts.
- `README.th.md`, `PROJECT_NOTICE.md`, `py.typed`, project metadata, and a test workflow for Python 3.10 to 3.13.
- `LICENSE`: the project is licensed under the TER-AI License 2.0 (SPDX `LicenseRef-TER-AI-2.0`). Source files carry an `SPDX-License-Identifier` line, and `pyproject.toml` declares the license (PEP 639, setuptools 77 or later). Before this, no license had been chosen. In Git history, main briefly carried TER-AI License 1.0 (`LicenseRef-TER-AI-1.0`, merge `1715f8a`) before it was replaced by 2.0; no release was ever made under 1.0, so 2.0 is the first license of any release.
- Tests (pytest): a completeness check over the Thai block, the examples inside sentences, `ห`/`ฮ`, `ๆ`, split sara am, the CLI, and `xfail` tests for the three open examples.

### Changed

- The whole-string `EXAMPLE_OVERRIDES` are removed. Results come from the table and the rules only, so a word gives the same result alone and inside a sentence.
- `เป็น`, `คำ` and `ฤดี` now follow the table (`aphn`, `cum`, `ruede`) until the open questions are decided.
- The version is defined once, in `romanizer_th/__init__.py`.
- `๕` is removed from the supplied row `ณ น ๕ → n`, which is now `ณ น → n`. `๕` is a digit like the others and gives `5`.

## 0.1.0

- First version: character map, whole-string example overrides, and a single-argument CLI.

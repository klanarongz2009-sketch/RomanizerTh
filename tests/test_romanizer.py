# SPDX-License-Identifier: LicenseRef-TER-AI-2.0
import subprocess
import sys
import unicodedata

import pytest

from romanizer_th import CHAR_MAP, IGNORED, PASS_THROUGH, REPEAT_MARK, __version__, romanize

THAI_BLOCK = [
    chr(cp) for cp in range(0x0E01, 0x0E5C) if unicodedata.name(chr(cp), None) is not None
]

# Supplied examples that the mapping table and the rules derive with no word list.
SUPPLIED_EXAMPLES = {
    "วันจันทร์": "wanjantr",
    "สวัสดี": "swasde",
    "อะไรใหม่": "oairihm",
    "อะไรใหม่ๆ": "oairihmm",
    "ดีๆ": "dee",
    "สามารถ": "samart",
}

# Supplied examples that disagree with the mapping table. The code follows the
# table; these stay as open questions until the scheme owner decides.
OPEN_QUESTIONS = [
    ("เป็น", "apn", "aphn", "the table maps ป to PH, the example uses p"),
    ("คำ", "kum", "cum", "the table maps ค to C, the example uses k"),
    ("ฤดี", "hruede", "ruede", "the example has a leading h that no table row gives"),
]


@pytest.mark.parametrize(("source", "expected"), SUPPLIED_EXAMPLES.items())
def test_supplied_examples(source, expected):
    assert romanize(source) == expected


@pytest.mark.parametrize(("source", "expected"), SUPPLIED_EXAMPLES.items())
def test_examples_are_the_same_inside_a_sentence(source, expected):
    assert romanize(f"{source} ก") == f"{expected} g"
    assert romanize(f"ก {source}") == f"g {expected}"


@pytest.mark.parametrize(("source", "example", "table", "reason"), OPEN_QUESTIONS)
def test_open_question_follows_the_table_today(source, example, table, reason):
    assert romanize(source) == table


@pytest.mark.parametrize(
    ("source", "example"),
    [
        pytest.param(src, ex, marks=pytest.mark.xfail(reason=f"open question: {why}"))
        for src, ex, _table, why in OPEN_QUESTIONS
    ],
)
def test_open_question_supplied_spelling(source, example):
    assert romanize(source) == example


def test_every_thai_code_point_is_classified_once():
    buckets = [set(CHAR_MAP) & set(THAI_BLOCK), set(IGNORED), {REPEAT_MARK}, set(PASS_THROUGH)]
    for char in THAI_BLOCK:
        hits = sum(char in bucket for bucket in buckets)
        assert hits == 1, f"U+{ord(char):04X} {char} is in {hits} buckets"


def test_no_thai_letter_leaks_into_output():
    text = "".join(THAI_BLOCK)
    leaked = {c for c in romanize(text) if 0x0E00 <= ord(c) <= 0x0E7F}
    assert leaked == set(PASS_THROUGH)


def test_every_code_point_is_documented():
    from pathlib import Path

    scheme_doc = (Path(__file__).resolve().parents[1] / "docs" / "SCHEME.md").read_text("utf-8")
    missing = [f"U+{ord(c):04X}" for c in THAI_BLOCK if f"U+{ord(c):04X}" not in scheme_doc]
    assert missing == []


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("ใหม่", "ihm"),
        ("ไหม", "ihm"),
        ("หนังสือ", "hnangsueo"),
        ("ฮา", "ha"),
        ("กรุงเทพมหานคร", "grungatpmhancr"),
    ],
)
def test_ho_hip_and_ho_nokhuk(source, expected):
    assert romanize(source) == expected


def test_mapping_groups():
    assert CHAR_MAP["ก"] == "g"
    assert CHAR_MAP["ข"] == "k"
    assert CHAR_MAP["ง"] == "ng"
    assert CHAR_MAP["ช"] == "ch"
    assert CHAR_MAP["ต"] == "th"
    assert CHAR_MAP["ณ"] == "n"
    assert CHAR_MAP["ฤ"] == "rue"
    assert CHAR_MAP["ไ"] == CHAR_MAP["ใ"] == "i"


def test_repeat_mark():
    assert romanize("ๆ") == ""
    assert romanize("ๆก") == "g"
    assert romanize("ดี ๆ") == "dee"
    assert romanize("ดีๆ ") == "dee "
    assert romanize("ดีๆกัน") == "deegan"
    assert romanize("Okๆ") == "Okk"
    # Non-ASCII Latin letters count too, composed or with a combining mark.
    assert romanize("caf\u00e9ๆ") == "caf\u00e9\u00e9"
    assert romanize("cafe\u0301ๆ") == "caf\u00e9\u00e9"
    # Fullwidth Latin letters are Latin too.
    assert romanize("caf\u00e9\uff21ๆ") == "caf\u00e9\uff21\uff21"


def test_unassigned_code_points_pass_through():
    gaps = "".join(chr(cp) for cp in range(0x0E3B, 0x0E3F))
    assert all(unicodedata.name(c, None) is None for c in gaps)
    assert romanize(gaps) == gaps


def test_split_sara_am_is_joined():
    assert romanize("ท\u0e4d\u0e32") == romanize("ทำ") == "tum"
    assert romanize("น\u0e4d\u0e49\u0e32") == romanize("น้ำ") == "num"


def test_digits_and_symbols():
    assert romanize("๑๒๓๐") == "1230"
    assert romanize("๕") == "5"
    assert romanize("๑๒๓๔๕") == "12345"
    assert romanize("๐๑๒๓๔๕๖๗๘๙") == "0123456789"
    assert romanize("ฯลฯ") == "ฯlฯ"
    assert romanize("฿100") == "฿100"
    assert romanize("ฤๅษี") == "ruese"


def test_tone_marks_are_ignored():
    assert romanize("ก่ก้ก๊ก๋") == "gggg"


def test_other_text_is_preserved():
    assert romanize("ก, ข!") == "g, k!"
    assert romanize("Hello 123") == "Hello 123"
    assert romanize("") == ""


def test_long_text():
    assert romanize("กา" * 5000) == "ga" * 5000


def test_rejects_non_string():
    with pytest.raises(TypeError):
        romanize(None)


def _cli(*args, stdin=None):
    return subprocess.run(
        [sys.executable, "-m", "romanizer_th", *args],
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    ).stdout


def test_cli_arguments():
    assert _cli("สวัสดี", "ครับ") == "swasde crab\n"


def test_cli_stdin():
    assert _cli(stdin="สวัสดี\nดีๆ\n") == "swasde\ndee\n"


def test_cli_respects_pythonioencoding():
    import os

    env = dict(os.environ, PYTHONIOENCODING="cp874")
    result = subprocess.run(
        [sys.executable, "-m", "romanizer_th"],
        input="สวัสดี\n".encode("cp874"),
        capture_output=True,
        env=env,
        check=True,
    )
    assert result.stdout.replace(b"\r\n", b"\n") == b"swasde\n"
    result = subprocess.run(
        [sys.executable, "-m", "romanizer_th", "฿๑"],
        capture_output=True,
        env=env,
        check=True,
    )
    assert result.stdout.strip() == "฿1".encode("cp874")


def test_cli_errors_handler_alone_keeps_utf8():
    import os

    env = dict(os.environ, PYTHONIOENCODING=":replace", PYTHONUTF8="0", LC_ALL="C", LANG="C")
    result = subprocess.run(
        [sys.executable, "-m", "romanizer_th"],
        input="ดีๆ\n".encode("utf-8"),
        capture_output=True,
        env=env,
        check=True,
    )
    assert result.stdout.replace(b"\r\n", b"\n") == b"dee\n"
    # The errors handler is applied: an invalid byte becomes U+FFFD, output stays UTF-8.
    result = subprocess.run(
        [sys.executable, "-m", "romanizer_th"],
        input="฿".encode("utf-8") + b"\xff\n",
        capture_output=True,
        env=env,
        check=True,
    )
    assert result.stdout.replace(b"\r\n", b"\n") == "฿\ufffd\n".encode("utf-8")


def test_cli_version():
    assert _cli("--version").strip() == f"romanizerth {__version__}"

# SPDX-License-Identifier: LicenseRef-TER-AI-1.0
"""RomanizerTh: custom Thai-to-Roman transliteration."""

from .core import normalize, romanize
from .scheme import CHAR_MAP, IGNORED, PASS_THROUGH, REPEAT_MARK

__all__ = ["CHAR_MAP", "IGNORED", "PASS_THROUGH", "REPEAT_MARK", "normalize", "romanize"]
__version__ = "0.2.0"

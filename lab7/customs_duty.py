"""Customs duty helpers, hardened against malformed input (Lab 7).

Every public function returns ``None`` when its input is invalid instead of
raising, so callers can simply test the result.
"""

import math
import re

# Plain ASCII decimal numbers only: rejects "nan", "inf", "1_000", unicode
# digits, hex, empty strings and anything with stray characters.
_NUMBER = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", re.ASCII)

MIN_CHAPTER = 1
MAX_CHAPTER = 97  # HS chapters run 01-97 (77 is reserved but unused)


def _to_amount(text):
    """Convert text to a finite, non-negative float, or return None."""
    if not isinstance(text, str):
        return None
    text = text.strip()
    if not _NUMBER.fullmatch(text):
        return None
    try:
        number = float(text)
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(number) or number < 0:
        return None
    return number


def parse_declaration(text):
    """Parse 'category:value' -> (lower-case category, value) or None."""
    if not isinstance(text, str):
        return None
    parts = text.split(":")
    if len(parts) != 2:
        return None
    category = parts[0].strip().lower()
    value = _to_amount(parts[1])
    if not category or value is None:
        return None
    return category, value


def duty_amount(text):
    """Parse 'value@rate' (rate in percent) -> duty amount or None."""
    if not isinstance(text, str):
        return None
    parts = text.split("@")
    if len(parts) != 2:
        return None
    value = _to_amount(parts[0])
    rate = _to_amount(parts[1])
    if value is None or rate is None:
        return None
    result = value * rate / 100
    if not math.isfinite(result):  # e.g. 1e308@1e308 overflows to inf
        return None
    return result


def hs_chapter(code):
    """Return the 2-digit HS chapter (1-97) of an HS code, or None."""
    if not isinstance(code, str):
        return None
    head = code.strip().split(".")[0]
    prefix = head[:2]
    if len(prefix) != 2 or not (prefix.isascii() and prefix.isdigit()):
        return None
    chapter = int(prefix)
    if not MIN_CHAPTER <= chapter <= MAX_CHAPTER:
        return None
    return chapter


def _ask(prompt, func):
    result = func(input(prompt))
    return result


def main():
    print("==== Running parse_declaration ====")
    result = _ask("Enter category:value (e.g. electronics:25000): ", parse_declaration)
    print("Category and Value:", result if result is not None else "Invalid input")

    print("\n==== Running duty_amount ====")
    result = _ask("Enter value@rate (e.g. 25000@20): ", duty_amount)
    print("Duty Amount:", result if result is not None else "Invalid input")

    print("\n==== Running hs_chapter ====")
    result = _ask("Enter an HS code (e.g. 8517.12): ", hs_chapter)
    print("Chapter:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()

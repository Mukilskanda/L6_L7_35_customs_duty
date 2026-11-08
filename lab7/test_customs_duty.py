import math

from hypothesis import given, strategies as st
from customs_duty import parse_declaration, duty_amount, hs_chapter

# Anything a caller (or attacker) might pass in: text, None, numbers, bytes, lists.
anything = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.binary(),
    st.lists(st.integers()),
)

# Realistic-looking but hostile strings built from the characters that matter.
tricky_text = st.text(alphabet=":@. \t\n-+eE0123456789abcINFnan_", max_size=20)


# ---------------------------------------------------------------- no-crash
@given(st.text() | st.none())
def test_parse_declaration_no_crash(s):
    try:
        parse_declaration(s)
    except Exception as e:
        assert False, f"parse_declaration crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_duty_amount_no_crash(s):
    try:
        duty_amount(s)
    except Exception as e:
        assert False, f"duty_amount crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_hs_chapter_no_crash(s):
    try:
        hs_chapter(s)
    except Exception as e:
        assert False, f"hs_chapter crashed with: {e!r} for input {s!r}"


# ------------------------------------------- no-crash, wider input types
@given(anything | tricky_text)
def test_parse_declaration_any_type_no_crash(s):
    try:
        parse_declaration(s)
    except Exception as e:
        assert False, f"parse_declaration crashed with: {e!r} for input {s!r}"


@given(anything | tricky_text)
def test_duty_amount_any_type_no_crash(s):
    try:
        duty_amount(s)
    except Exception as e:
        assert False, f"duty_amount crashed with: {e!r} for input {s!r}"


@given(anything | tricky_text)
def test_hs_chapter_any_type_no_crash(s):
    try:
        hs_chapter(s)
    except Exception as e:
        assert False, f"hs_chapter crashed with: {e!r} for input {s!r}"


# ------------------------------------------------ output-shape properties
@given(tricky_text | st.text())
def test_parse_declaration_output_is_valid_or_none(s):
    result = parse_declaration(s)
    if result is not None:
        category, value = result
        assert isinstance(category, str) and category != ""
        assert category == category.strip().lower()
        assert math.isfinite(value) and value >= 0


@given(tricky_text | st.text())
def test_duty_amount_output_is_valid_or_none(s):
    result = duty_amount(s)
    if result is not None:
        assert math.isfinite(result) and result >= 0


@given(tricky_text | st.text())
def test_hs_chapter_output_is_valid_or_none(s):
    result = hs_chapter(s)
    if result is not None:
        assert isinstance(result, int) and 1 <= result <= 97


# ----------------------------------------- correctness on valid input
@given(
    st.text(alphabet=st.characters(whitelist_categories=("Ll", "Lu")), min_size=1),
    st.floats(min_value=0, max_value=1e12, allow_nan=False),
)
def test_parse_declaration_roundtrip(category, value):
    result = parse_declaration(f"{category}:{value}")
    assert result == (category.lower(), value)


@given(
    st.floats(min_value=0, max_value=1e9, allow_nan=False),
    st.floats(min_value=0, max_value=100, allow_nan=False),
)
def test_duty_amount_matches_formula(value, rate):
    result = duty_amount(f"{value}@{rate}")
    assert result is not None
    assert math.isclose(result, value * rate / 100, rel_tol=1e-9, abs_tol=1e-9)


@given(st.integers(min_value=1, max_value=97), st.integers(min_value=0, max_value=99))
def test_hs_chapter_valid_codes(chapter, sub):
    assert hs_chapter(f"{chapter:02d}{sub:02d}.{sub:02d}") == chapter


# ------------------------------------------- explicit regression cases
def test_known_bad_inputs_are_rejected():
    for bad in [None, "", ":", "a:", ":5", "a:b", "a:1:2", "a:nan", "a:inf",
                "a:-5", "a b"]:
        assert parse_declaration(bad) is None, bad
    for bad in [None, "", "@", "5@", "@5", "5@5@5", "x@y", "5@nan", "5@inf",
                "-5@10", "5@-10", "1e308@1e308"]:
        assert duty_amount(bad) is None, bad
    for bad in [None, "", ".", "5", "ab.12", "00.1", "98.1", "-1.2", "+8.1",
                "٨٥١٧", "   "]:
        assert hs_chapter(bad) is None, bad


def test_known_good_inputs():
    assert parse_declaration("Electronics : 25000") == ("electronics", 25000.0)
    assert duty_amount("25000@20") == 5000.0
    assert hs_chapter("8517.12") == 85
    assert hs_chapter(" 0101.21 ") == 1

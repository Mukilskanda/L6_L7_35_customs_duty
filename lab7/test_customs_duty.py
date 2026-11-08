from hypothesis import given, strategies as st
from customs_duty import parse_declaration, duty_amount, hs_chapter

@given(st.text() | st.none())
def test_parse_declaration_no_crash(s):

@given(st.text() | st.none())
def test_duty_amount_no_crash(s):

@given(st.text() | st.none())
def test_hs_chapter_no_crash(s):

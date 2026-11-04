import pytest
from customs_duty import duty_rate, total_duty, clearance_channel

#Example test cases:
def test_books_are_duty_free():
    assert duty_rate("books", "FTA") == 0

def test_low_value_personal_import():
    assert total_duty("books", 500, "US", False) == 0

#Write the rest of the test cases so that the code is 90- 100% covered.

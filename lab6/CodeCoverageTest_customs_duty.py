import pytest
from customs_duty import duty_rate, total_duty, clearance_channel

# Lab 6 - Step 5: test cases written to reach >= 90% CODE (line) coverage.


# ---- duty_rate ----
def test_books_are_duty_free():
    assert duty_rate("books", "FTA") == 0


def test_prohibited_category_raises():
    with pytest.raises(ValueError):
        duty_rate("weapons", "US")


def test_electronics_fta_rate():
    assert duty_rate("electronics", "FTA") == 0.10


def test_electronics_non_fta_rate():
    assert duty_rate("electronics", "US") == 0.20


def test_clothing_fta_rate():
    assert duty_rate("clothing", "FTA") == 0.05


def test_clothing_non_fta_rate():
    assert duty_rate("clothing", "US") == 0.12


def test_other_category_default_rate():
    assert duty_rate("furniture", "US") == 0.15


# ---- total_duty ----
def test_low_value_personal_import():
    assert total_duty("books", 500, "US", False) == 0


def test_negative_value_raises():
    with pytest.raises(ValueError):
        total_duty("books", -1, "US", False)


def test_gift_under_exemption_is_free():
    assert total_duty("electronics", 4000, "US", True) == 0


def test_gift_over_exemption_taxes_only_the_excess():
    # (10000 - 5000) * 0.20 = 1000
    assert total_duty("electronics", 10000, "US", True) == pytest.approx(1000)


def test_personal_import_over_threshold_is_taxed():
    # 2000 * 0.20 = 400
    assert total_duty("electronics", 2000, "US", False) == pytest.approx(400)


def test_minimum_duty_of_50_applies():
    # (5100 - 5000) * 0.05 = 5 -> raised to the 50 minimum
    assert total_duty("clothing", 5100, "FTA", True) == 50


# ---- clearance_channel ----
def test_prohibited_is_refused():
    assert clearance_channel(100, "narcotics", True) == "refuse"


def test_very_high_value_is_inspected():
    assert clearance_channel(100001, "books", True) == "inspect"


def test_high_value_without_documents_is_inspected():
    assert clearance_channel(30000, "books", False) == "inspect"


def test_normal_shipment_is_green():
    assert clearance_channel(500, "books", True) == "green"

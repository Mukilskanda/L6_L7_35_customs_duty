import pytest
from customs_duty import duty_rate, total_duty, clearance_channel

# Lab 6 - Step 7: test cases written to reach >= 90% BRANCH coverage.
# Every if/elif is exercised both True and False, including edge values.


# ---- duty_rate: every decision both ways ----
@pytest.mark.parametrize("category", ["weapons", "narcotics"])
def test_each_prohibited_category_raises(category):
    with pytest.raises(ValueError):
        duty_rate(category, "FTA")


@pytest.mark.parametrize("category, origin, expected", [
    ("electronics", "FTA", 0.10),
    ("electronics", "US", 0.20),
    ("clothing", "FTA", 0.05),
    ("clothing", "US", 0.12),
    ("books", "FTA", 0),
    ("books", "US", 0),
    ("furniture", "FTA", 0.15),
    ("furniture", "US", 0.15),
])
def test_duty_rate_table(category, origin, expected):
    assert duty_rate(category, origin) == expected


# ---- total_duty: every decision both ways ----
def test_negative_value_raises():
    with pytest.raises(ValueError):
        total_duty("books", -1, "US", False)


def test_zero_value_is_not_negative():
    assert total_duty("books", 0, "US", False) == 0


def test_gift_at_exemption_boundary_is_free():
    assert total_duty("electronics", 5000, "US", True) == 0


def test_gift_just_over_exemption_is_taxed_on_excess():
    # (5001 - 5000) * 0.20 = 0.2 -> minimum duty 50
    assert total_duty("electronics", 5001, "US", True) == 50


def test_gift_large_value_taxes_only_excess():
    assert total_duty("electronics", 10000, "US", True) == pytest.approx(1000)


def test_personal_at_threshold_is_free():
    assert total_duty("electronics", 1000, "US", False) == 0


def test_personal_just_over_threshold_gets_minimum_duty():
    # 1001 * 0.20 = 200.2 (no minimum), clothing FTA: 1001 * 0.05 = 50.05
    assert total_duty("clothing", 1001, "FTA", False) == pytest.approx(50.05)


def test_personal_large_value_is_taxed():
    assert total_duty("electronics", 2000, "US", False) == pytest.approx(400)


def test_zero_rate_category_gives_zero_duty_not_minimum():
    # duty == 0 must NOT be raised to 50
    assert total_duty("books", 5000, "US", False) == 0


def test_duty_below_50_is_raised_to_minimum():
    assert total_duty("clothing", 5100, "FTA", True) == 50


def test_duty_exactly_50_is_unchanged():
    # (6000 - 5000) * 0.05 = 50
    assert total_duty("clothing", 6000, "FTA", True) == pytest.approx(50)


def test_prohibited_category_raises_through_total_duty():
    with pytest.raises(ValueError):
        total_duty("weapons", 2000, "US", False)


# ---- clearance_channel: every decision both ways ----
def test_prohibited_is_refused():
    assert clearance_channel(100, "weapons", True) == "refuse"


def test_prohibited_beats_value_rules():
    assert clearance_channel(500000, "narcotics", False) == "refuse"


def test_value_over_100000_is_inspected_even_with_documents():
    assert clearance_channel(100001, "books", True) == "inspect"


def test_value_exactly_100000_with_documents_is_green():
    assert clearance_channel(100000, "books", True) == "green"


def test_value_over_20000_without_documents_is_inspected():
    assert clearance_channel(20001, "books", False) == "inspect"


def test_value_over_20000_with_documents_is_green():
    assert clearance_channel(50000, "books", True) == "green"


def test_value_exactly_20000_without_documents_is_green():
    assert clearance_channel(20000, "books", False) == "green"


def test_small_shipment_without_documents_is_green():
    assert clearance_channel(100, "books", False) == "green"

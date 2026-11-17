import pytest

from src.cli import ask, budget_warnings, main, parse_amount, parse_months

# parse_amount 

@pytest.mark.parametrize("text, expected", [
    ("250", 250.0),
    ("99.50", 99.5),
    ("  100  ", 100.0),
    ("€600", 600.0),
    ("1,200", 1200.0),
    ("0", 0.0),
])
def test_parse_amount_accepts_valid_amounts(text, expected):
    assert parse_amount(text) == expected

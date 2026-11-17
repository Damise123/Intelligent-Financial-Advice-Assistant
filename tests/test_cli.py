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


@pytest.mark.parametrize("text", ["", "   ", "abc", "-50", "nan", "inf"])
def test_parse_amount_rejects_invalid_amounts(text):
    with pytest.raises(ValueError):
        parse_amount(text)


# parse_months 

@pytest.mark.parametrize("text, expected", [("1", 1), ("6", 6), (" 12 ", 12)])
def test_parse_months_accepts_positive_whole_numbers(text, expected):
    assert parse_months(text) == expected


@pytest.mark.parametrize("text", ["", "0", "-3", "2.5", "six"])
def test_parse_months_rejects_invalid_deadlines(text):
    with pytest.raises(ValueError):
        parse_months(text)


# ask: re-prompting 

def fake_input(answers):
    answers = iter(answers)
    return lambda prompt="": next(answers)


def test_ask_keeps_asking_until_input_is_valid(capsys):
    value = ask("Income: ", "amount", fake_input(["abc", "-5", "300"]))
    assert value == 300.0
    assert capsys.readouterr().out.count("Invalid input") == 2

    
# warnings 

def test_warns_when_spending_exceeds_income():
    budget = {"income": 800, "essential_expenses": 700, "optional_spending": 200,
              "current_savings": 0, "target": 600, "deadline_months": 4}
    assert "Your spending is higher than your income." in budget_warnings(budget)


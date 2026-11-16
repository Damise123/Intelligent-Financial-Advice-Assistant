from src.placeholders import calculate, run_reasoning

FIELDS = [
    ("income", "Monthly income (EUR): ", "amount"),
    ("essential_expenses", "Essential monthly expenses (EUR): ", "amount"),
    ("optional_spending", "Optional monthly spending (EUR): ", "amount"),
    ("current_savings", "Current savings (EUR): ", "amount"),
    ("target", "Savings target (EUR): ", "amount"),
    ("deadline_months", "Deadline (whole months from now): ", "months"),
]


def parse_amount(text):
    """Turn user text into a money amount, or raise ValueError with a reason."""
    cleaned = text.strip().replace("€", "").replace(",", "")
    if cleaned == "":
        raise ValueError("Please enter a value.")
    try:
        value = float(cleaned)
    except ValueError:
        raise ValueError("Please enter a number, for example 250 or 99.50.")
    if value != value or value in (float("inf"), float("-inf")):
        raise ValueError("Please enter a normal number.")
    if value < 0:
        raise ValueError("Amounts cannot be negative.")
    return round(value, 2)


def parse_months(text):
    """Turn user text into a deadline in whole months, or raise ValueError."""
    cleaned = text.strip()
    if cleaned == "":
        raise ValueError("Please enter a value.")
    try:
        value = int(cleaned)
    except ValueError:
        raise ValueError("Please enter a whole number of months, for example 6.")
    if value <= 0:
        raise ValueError("The deadline must be at least 1 month.")
    return value

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


PARSERS = {"amount": parse_amount, "months": parse_months}


# Asking the user

def ask(prompt, kind, input_func=input):
    """Keep asking until the user gives a valid value, then return it."""
    parser = PARSERS[kind]
    while True:
        try:
            return parser(input_func(prompt))
        except ValueError as error:
            print(f"  Invalid input: {error}")

def collect_budget(input_func=input):
    """Ask for all six figures and return them as a dictionary."""
    print("\nEnter your monthly budget and savings goal.")
    return {key: ask(prompt, kind, input_func) for key, prompt, kind in FIELDS}


def budget_warnings(budget):
    """Point out unusual but valid inputs. These are not errors: the reasoning
    engine still explains them, but the user may have made a typo."""
    warnings = []
    spending = budget["essential_expenses"] + budget["optional_spending"]
    if spending > budget["income"]:
        warnings.append("Your spending is higher than your income.")
    if budget["current_savings"] >= budget["target"]:
        warnings.append("Your current savings already cover the target.")
    return warnings


# Showing the result 

def show_result(budget, facts, result):
    """Print the figures, the conclusion and the explanation."""
    print("\n========== Assessment ==========")
    print(f"Target:                 EUR {budget['target']:.2f}")
    print(f"Still to save:          EUR {facts['remaining_target']:.2f}")
    print(f"You can save per month: EUR {facts['monthly_savings']:.2f}")
    print(f"Needed per month:       EUR {facts['needed_per_month']:.2f}")
    print(f"Deadline:               {budget['deadline_months']} months")
    print(f"\nConclusion: {result['conclusion']}")
    print("\nWhy: these rules fired:")
    for rule in result["rules_fired"]:
        print(f"  - {rule}")
    print("================================")


def assess(budget):
    """Connect the modules: budget -> calculations -> reasoning -> display."""
    for warning in budget_warnings(budget):
        print(f"  Note: {warning}")
    facts = calculate(budget)
    result = run_reasoning(facts)
    show_result(budget, facts, result)


def main(input_func=input):
    """Run the assistant until the user quits."""
    print("Intelligent Financial Advice Assistant")
    budget = collect_budget(input_func)
    assess(budget)
    while True:
        print("\n[c] change one figure   [n] new assessment   [q] quit")
        choice = input_func("Choose an option: ").strip().lower()
        if choice == "c":
            key, prompt, kind = choose_field(input_func)
            budget[key] = ask(prompt, kind, input_func)
            assess(budget)
        elif choice == "n":
            budget = collect_budget(input_func)
            assess(budget)
        elif choice == "q":
            print("Goodbye.")
            return
        else:
            print("  Invalid input: type c, n or q.")

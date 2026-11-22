def calculate_remaining_target(target, current_savings):
    """Calculate how much more money is needed."""
    return round(max(target - current_savings, 0), 2)


def calculate_monthly_balance(income, essential_expenses, optional_spending):
    """Calculate the money left after monthly expenses."""
    return round(income - essential_expenses - optional_spending, 2)


def calculate_required_monthly_savings(remaining_target, months):
    """Calculate the monthly savings needed to meet the deadline."""
    if months <= 0:
        raise ValueError("The number of months must be greater than zero.")

    return remaining_target / months


def calculate(budget):
    """Return the three figures needed by the reasoning module."""
    remaining_target = calculate_remaining_target(
        budget["target"],
        budget["current_savings"]
    )

    monthly_savings = calculate_monthly_balance(
        budget["income"],
        budget["essential_expenses"],
        budget["optional_spending"]
    )

    needed_per_month = calculate_required_monthly_savings(
        remaining_target,
        budget["deadline_months"]
    )

    return {
        "remaining_target": remaining_target,
        "monthly_savings": monthly_savings,
        "needed_per_month": needed_per_month
    }

import math

from src.Calculations import calculate


def run_reasoning(facts):
    """Return a conclusion and the rules that led to it."""
    if facts["remaining_target"] == 0:
        return {
            "conclusion": "You already have enough saved for this goal.",
            "rules_fired": ["R0: current savings cover the target"],
        }

    if facts["monthly_savings"] <= 0:
        return {
            "conclusion": (
                "Your expenses use up all of your income, so extending the "
                "deadline alone will not help. You need to cut spending or "
                "increase income."
            ),
            "rules_fired": [
                "R3: expenses are greater than or equal to income"
            ],
        }

    if facts["monthly_savings"] >= facts["needed_per_month"]:
        return {
            "conclusion": "Your goal is achievable by the deadline.",
            "rules_fired": [
                "R1: monthly savings cover the amount needed"
            ],
        }

    shortfall = facts["needed_per_month"] - facts["monthly_savings"]
    months = math.ceil(
        facts["remaining_target"] / facts["monthly_savings"]
    )

    return {
        "conclusion": (
            f"You are short by EUR {shortfall:.2f} per month. "
            f"At your current rate you would reach the goal "
            f"in {months} months."
        ),
        "rules_fired": [
            "R2: monthly shortfall identified",
            "R4: suggest a longer deadline based on current savings rate",
        ],
    }
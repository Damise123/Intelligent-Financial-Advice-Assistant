import math


def calculate(budget):
  """Work out the starting figures the reasoning engine needs."""
    monthly_savings = (
        budget["income"] - budget["essential_expenses"] - budget["optional_spending"]
    )
remaining_target = max(budget["target"] - budget["current_savings"], 0)
needed_per_month = remaining_target / budget["deadline_months"]
return {
        "monthly_savings": monthly_savings,
        "remaining_target": remaining_target,
        "needed_per_month": needed_per_month,
    }



def run_reasoning(facts):
   """Return a conclusion and the rules that led to it (simplified rules)."""
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
        "rules_fired": ["R3: expenses are greater than or equal to income"],
        }
    if facts["monthly_savings"] >= facts["needed_per_month"]:
        return {
            "conclusion": "Your goal is achievable by the deadline.",
            "rules_fired": ["R1: monthly savings cover the amount needed"],
        }
    shortfall = facts["needed_per_month"] - facts["monthly_savings"]
    months = math.ceil(facts["remaining_target"] / facts["monthly_savings"])
    return {
        "conclusion": (
            f"You are short by EUR {shortfall:.2f} per month. At your current "
            f"rate you would reach the goal in {months} months."
        ),










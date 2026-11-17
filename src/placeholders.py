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


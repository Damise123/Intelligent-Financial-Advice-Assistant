import math

def calculate(budget):
  """Work out the starting figures the reasoning engine needs."""
    monthly_savings = (
        budget["income"] - budget["essential_expenses"] - budget["optional_spending"]
    )
remaining_target = max(budget["target"] - budget["current_savings"], 0)

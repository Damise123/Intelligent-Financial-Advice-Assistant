import math

from src.inference_engine import Rule


# Rule fires when you've already saved enough
r0 = Rule(
    name="R0",
    description="Current savings cover the target",
    premises=["remaining_target"],
    condition=lambda f: f["remaining_target"] == 0,
    conclude=lambda f: {"conclusion": "You already have enough saved for this goal."},
)

# If monthly_savings is known and its 0 or less, then connclude that a longer deadline wont fix it
r3 = Rule(
    name="R3",
    description="Expenses are greater than or equal to income",
    premises=["monthly_savings"],
    condition=lambda f: f["monthly_savings"] <= 0,
    conclude=lambda f: {
        "conclusion": "Your expenses use up all of your income, so extending the deadline "
                      "alone will not help. You need to cut spending or increase income."
    },
)
# If you save at least whats needed each month, then the goal is achievable
r1 = Rule(
    name="R1",
    description="Monthly savings cover the amount needed",
    premises=["monthly_savings", "needed_per_month"],
    condition=lambda f: f["monthly_savings"] > 0
    and f["monthly_savings"] >= f["needed_per_month"],
    conclude=lambda f: {"conclusion": "Your goal is achievable by the deadline."},
)

# If you save something each month but less than you need then shortfall shows how much you're short each month
r2 = Rule(
    name="R2",
    description="Monthly shortfall identified",
    premises=["monthly_savings", "needed_per_month"],
    condition=lambda f: 0 < f["monthly_savings"] < f["needed_per_month"],
    conclude=lambda f: {"shortfall": f["needed_per_month"] - f["monthly_savings"]},
)

# uses the shortfall from R2 to work out how many months the goal would take at the current rate
r4 = Rule(
    name="R4",
    description="Suggest a longer deadline based on current savings rate",
    premises=["shortfall", "monthly_savings", "remaining_target"],
    conclude=lambda f: {
        "suggested_months": math.ceil(f["remaining_target"] / f["monthly_savings"]),
        "conclusion": f"You are short by EUR {f['shortfall']:.2f} per month. "
                      f"At your current rate you would reach the goal in "
                      f"{math.ceil(f['remaining_target'] / f['monthly_savings'])} months.",
    },
)

# order matters the engine checks rules top to bottom
RULES = [r0, r3, r1, r2, r4]
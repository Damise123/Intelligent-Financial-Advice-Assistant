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
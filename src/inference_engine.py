"""Forward chaining inference engine with an explanation trace.

The engine knows nothing about money. It takes a dictionary of starting
facts and a list of Rule objects (the knowledge base), and keeps firing
rules until no rule can add anything new. Every time a rule fires, the
engine records which facts it used and which facts it added, so that any
conclusion can be traced back to the starting facts.

AIMA view:
    State       -> the current set of known facts (a dict: name -> value)
    Action      -> firing one rule whose premises are satisfied
    Goal test   -> no rule can fire any more (a fixed point is reached)
    Knowledge   -> the list of Rule objects
    Reasoning   -> data-driven forward chaining (modus ponens, repeated)
"""

from dataclasses import dataclass, field
from typing import Callable

@dataclass
class Rule:
    """IF all `premises` are known AND `condition(facts)` is true
    THEN add the facts returned by `conclude(facts)`.

    name        short id shown in explanations, e.g. "R2"
    description plain-English meaning of the rule
    premises    names of facts that must already be known
    condition   extra test on the fact values (defaults to always true)
    conclude    returns a dict of new facts to add
    """
    
    name:str 
    description: str
    premises: list
    conclude: Callable[[dict], dict]
    condition: Callable[[dict], bool] = lambda facts: True
    

@dataclass
class Firing:
    step: int
    rule: Rule 
    used: dict
    added: dict
    
@dataclass
class InferenceResult:
    facts: dict
    trace: list = field(default_factory=list)
    initial: set = field(default_factory=set)
    
    def fired_rule_names(self):
        return[firing.rule.name for firing in self.trace]
    
def can_fire(rule, facts):
    """A rule can fire when every premise is known and its condition holds."""
    if not all(premise in facts for premise in rule.premises):
        return False
    return bool(rule.condition(facts))
    

def forward_chain(initial_facts, rules, max_steps=100):
    """Apply rules to the facts until nothing new can be inferred.

    - Rules are tried in the order they appear in the knowledge base, so
      list order is the conflict-resolution strategy.
    - Each rule fires at most once (refraction), which guarantees the loop
      stops even if a rule's condition stays true.
    - Facts are never overwritten: if a rule tries to set a fact that is
      already known, only its genuinely new facts are added. This keeps
      reasoning monotonic, as in propositional forward chaining.
    """
    facts = dict(initial_facts)
    result = InferenceResult(facts=facts, initial=set(initial_facts))
    fired = set()

    changed = True
    while changed:
        changed = False
        for rule in rules:
            if rule.name in fired or not can_fire(rule, facts):
                continue
            new_facts = {
                key: value
                for key, value in rule.conclude(facts).items()
                if key not in facts
            }
            fired.add(rule.name)
            if not new_facts:
                continue
            used = {premise: facts[premise] for premise in rule.premises}
            facts.update(new_facts)
            result.trace.append(
                Firing(len(result.trace) + 1, rule, used, new_facts)
            )
            changed = True
            if len(result.trace) >= max_steps:
                raise RuntimeError("Too many rule firings; check the rules.")
            # Start again from the first rule so higher-priority rules
            # see the new facts before lower-priority ones.
            break
    return result


def explain(result, fact_name):
    """Return the firings that led to `fact_name`, in the order they fired.

    This walks backwards from the conclusion: find the rule that added the
    fact, then the rules that added that rule's premises, and so on until
    only starting facts remain. Rules that fired but did not contribute to
    this conclusion are left out.
    """
    producer = {}
    for firing in result.trace:
        for key in firing.added:
            producer[key] = firing

    needed = []
    seen = set()

    def visit(name):
        firing = producer.get(name)
        if firing is None or firing.step in seen:
            return  # a starting fact, or already explained
        seen.add(firing.step)
        for premise in firing.rule.premises:
            visit(premise)
        needed.append(firing)

    visit(fact_name)
    return sorted(needed, key=lambda firing: firing.step)


def format_value(value):
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def describe_firing(firing):
    """One readable line for the CLI, e.g.
    'R2 Monthly shortfall: used needed_per_month=150.00, ... -> shortfall=50.00'
    """
    used = ", ".join(f"{k}={format_value(v)}" for k, v in firing.used.items())
    added = ", ".join(
        "conclusion reached" if k == "conclusion" else f"{k}={format_value(v)}"
        for k, v in firing.added.items()
    )
    return f"{firing.rule.name} {firing.rule.description}: used {used} -> {added}"
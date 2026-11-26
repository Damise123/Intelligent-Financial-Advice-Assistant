"""Tests for the generic forward chaining engine, using toy rules."""

from src.inference_engine import Rule, explain, forward_chain


def make(name, premises, adds, condition=lambda f: True):
    return Rule(name, name, premises, lambda f: dict(adds), condition)


def test_chains_rules_to_reach_new_facts():
    rules = [make("B_to_C", ["b"], {"c": True}), make("A_to_B", ["a"], {"b": True})]
    result = forward_chain({"a": True}, rules)
    assert result.facts["c"] is True
    # A_to_B must fire before B_to_C even though it is listed second
    assert result.fired_rule_names() == ["A_to_B", "B_to_C"]


def test_rule_does_not_fire_when_premise_missing():
    result = forward_chain({"a": True}, [make("R", ["x"], {"y": True})])
    assert "y" not in result.facts
    assert result.trace == []


def test_rule_does_not_fire_when_condition_false():
    rule = make("R", ["n"], {"big": True}, condition=lambda f: f["n"] > 10)
    assert "big" not in forward_chain({"n": 3}, [rule]).facts
    assert forward_chain({"n": 30}, [rule]).facts["big"] is True


def test_each_rule_fires_once_and_engine_stops():
    # Condition is always true; refraction stops it looping forever.
    counter = Rule("R", "count", [], lambda f: {f"seen_{len(f)}": True})
    result = forward_chain({}, [counter])
    assert result.fired_rule_names() == ["R"]


def test_existing_facts_are_not_overwritten():
    result = forward_chain({"a": 1}, [make("R", [], {"a": 2, "b": 3})])
    assert result.facts == {"a": 1, "b": 3}
    assert result.trace[0].added == {"b": 3}


def test_input_facts_are_not_modified():
    start = {"a": True}
    forward_chain(start, [make("R", ["a"], {"b": True})])
    assert start == {"a": True}


def test_trace_records_used_and_added_facts():
    result = forward_chain({"a": 5}, [make("R", ["a"], {"b": 10})])
    firing = result.trace[0]
    assert firing.used == {"a": 5}
    assert firing.added == {"b": 10}


def test_explanation_only_includes_rules_that_led_to_the_fact():
    rules = [
        make("A_to_B", ["a"], {"b": True}),
        make("A_to_X", ["a"], {"x": True}),  # fires but is irrelevant
        make("B_to_GOAL", ["b"], {"goal": True}),
    ]
    result = forward_chain({"a": True}, rules)
    assert set(result.fired_rule_names()) == {"A_to_B", "A_to_X", "B_to_GOAL"}
    chain = [firing.rule.name for firing in explain(result, "goal")]
    assert chain == ["A_to_B", "B_to_GOAL"]


def test_explaining_a_starting_fact_needs_no_rules():
    result = forward_chain({"a": True}, [])
    assert explain(result, "a") == []

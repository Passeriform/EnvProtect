"""Define rulebook registry and usable rulesets.

RuleSets defined in this module can be applied over repositories to mark secrets.
"""
from envprotect.exception.rulebook import RuleSetNotFoundError
from .rulebook import RULESET_REGISTRY, RULESET_DEPS_MAP, RuleFactory, RuleSet
from .aws import AWSRuleSet

__all__ = [
    "RuleSetNotFoundError",
    "RULESET_REGISTRY", "RULESET_DEPS_MAP", "RuleFactory", "RuleSet",
    "AWSRuleSet",
]

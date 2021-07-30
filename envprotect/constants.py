"""Define constants and enums to be used across EnvProtect."""
from enum import Enum


class RuleSets(str, Enum):
    """Define ruleset names mapping."""

    AWS_RULESET = "AWS"

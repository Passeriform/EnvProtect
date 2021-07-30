"""Rulebook definition and registry module.

This module defines rules and its container rulesets, provides a partial
blueprint class and rulefactory to register external rules.
"""
from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import List, Dict, Any, Callable, Type, TypeVar, Union, overload
from envprotect.core.detection import DetectionResult
from envprotect.exception.rulebook import RuleSetNotFoundError

# pylint: disable=invalid-name
T = TypeVar("T", bound="RuleSet")
# pylint: enable=invalid-name

RULESET_REGISTRY: Dict[str, Type[RuleSet]]
"""Maintain global ruleset registry."""

RULESET_DEPS_MAP: Dict[str, str]
"""Maintain mapping from dependency name to ruleset name."""


class RuleSet(metaclass=ABCMeta):
    """Define ruleset as a collection for similar rules."""

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        """Act as placeholder abstract method."""

    @overload
    @abstractmethod
    def detect_secrets(self,
                       target: Union[str, bytes],
                       apply: bool) -> DetectionResult: ...

    @overload
    @abstractmethod
    def detect_secrets(self,
                       target: Union[str, bytes],
                       apply: bool,
                       *args: Any,
                       **kwargs: Any) -> DetectionResult: ...

    @abstractmethod
    def detect_secrets(self,
                       target: Union[str, bytes],
                       apply: bool,
                       *args: Any,
                       **kwargs: Any) -> DetectionResult:
        """Act as placeholder abstract method.

        Args:
            target: Data string to be used for detection.
            apply: Flag to allow raising detection to apply.

        Returns:
            DetectionResult instance with detections listed.
        """


class RuleFactory:
    """Factory class for creating ruleset."""

    @classmethod
    def fetch_rule_set(cls, ruleset_name: str, **kwargs: Dict[str, Any]) -> RuleSet:
        """Create a new ruleset instance using factory.

        Fetch appropriate ruleset from registry and return its instance.

        Args:
            ruleset_name: Name of the ruleset to instantiate.

        Returns:
            An instance of created rule.
        """
        try:
            exec_class: Type[RuleSet] = RULESET_REGISTRY[ruleset_name]
            ruleset_instance = exec_class(**kwargs)
            return ruleset_instance
        except KeyError as error:
            formatted_registry_keys: str = '\n'.join([f"- {key}" for key in RULESET_REGISTRY.keys()])
            raise RuleSetNotFoundError(message=f"""
RuleSet isn't present in the registry yet. Consider registering using the `register` class-method.

Existing rule sets are as follows:\n{formatted_registry_keys}
            """) from error

    @classmethod
    def register(cls, ruleset_name: str, deps_list: List[str]) -> Callable[[Type[T]], Type[T]]:
        """Register ruleset class to rulebook registry using factory.

        Fetch appropriate ruleset from registry and return its instance.

        Args:
            ruleset_name: Name of the ruleset class to register.
            deps_list: List of actual dependency names corresponding to ruleset.

        Returns:
            The callable ruleset class object.
        """
        def inner_wrapper(wrapped_class: Type[T]) -> Type[T]:
            if ruleset_name in RULESET_REGISTRY:
                print("""
RuleSet already registered. This will override the previous rule.
                """)
            RULESET_REGISTRY[ruleset_name] = wrapped_class
            for dependency in deps_list:
                RULESET_DEPS_MAP[dependency] = ruleset_name
            return wrapped_class

        return inner_wrapper

"""Define exceptions for Rulebook."""


class RuleSetNotFoundError(Exception):
    """Raise when ruleset isn't found in registry."""

    def __init__(self, expression: str = '', message: str = '') -> None:
        """Initialize RuleSetNotFoundError instance.

        Args:
            expression: Define expression for exception.
            message: Message string for exception.
        """
        super().__init__()
        self.expression = expression
        self.message = message

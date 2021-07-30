"""Define exceptions for Dependencies."""


class StringParseException(Exception):
    """Raise on failure to parse string into dependency object."""

    def __init__(self, expression: str = '', message: str = '') -> None:
        """Initialize StringParseException instance.

        Args:
            expression: Define expression for exception.
            message: Message string for exception.
        """
        super().__init__()
        self.expression = expression
        self.message = message

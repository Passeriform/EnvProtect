"""Define exceptions for Report."""


class UnknownOutputStreamError(Exception):
    """Raise when output file is not defined."""

    def __init__(self, expression: str = '', message: str = '') -> None:
        """Initialize UnknownOutputStreamError instance.

        Args:
            expression: Define expression for exception.
            message: Message string for exception.
        """
        super().__init__()
        self.expression = expression
        self.message = message

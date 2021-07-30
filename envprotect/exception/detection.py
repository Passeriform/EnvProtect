"""Define exceptions for Detection."""


class DetectionException(Exception):
    """Raise when a detection throws an exception."""

    def __init__(self, expression: str = '', message: str = '') -> None:
        """Initialize DetectionException instance.

        Args:
            expression: Define expression for exception.
            message: Message string for exception.
        """
        super().__init__()
        self.expression = expression
        self.message = message

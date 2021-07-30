"""Define exceptions for Git."""


class GitignoreNotFoundError(Exception):
    """Raise to signify a lack of gitignore file."""

    def __init__(self, expression: str = '', message: str = '') -> None:
        """Initialize GitignoreNotFoundError instance.

        Args:
            expression: Define expression for exception.
            message: Message string for exception.
        """
        super().__init__()
        self.expression = expression
        self.message = message

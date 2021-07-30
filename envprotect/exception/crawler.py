"""Define exceptions for Crawler."""
from typing import Optional


class CrawlException(Exception):
    """Wrapper exception for exceptions raised inside a crawler."""

    def __init__(self, expression: str = '', message: str = '', from_exc: Optional[BaseException] = None) -> None:
        """Initialize CrawlException instance.

        Args:
            expression: Define expression for exception.
            message: Message string for exception.
            from_exc: Define __cause__ as parameter.
        """
        super().__init__()
        self.expression = expression
        self.message = message
        self.__cause__ = from_exc

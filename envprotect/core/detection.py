"""Define detections and corresponding result type wrapper."""
from typing import List, TypeVar, Any, Optional
from envprotect.core.result import Result, ResultType
from envprotect.exception.detection import DetectionException

# pylint: disable=invalid-name
K = TypeVar('K')
E = TypeVar('E', bound=DetectionException)
# pylint: enable=invalid-name


# TODO: Define this interface with docstrings.
class Detection:
    """Define detection class as a utility wrapper over detect_secrets."""

    # TODO: Define this interface
    def __init__(self, result: Optional[ResultType] = None) -> None:
        """Initialize new Detection object.

        Args:
            result: Create detection from existing result.
        """
        self.result = result

    # TODO: Define this interface
    # TODO: Change to ApplyResult
    def apply(self) -> ResultType:
        """Apply the detections.

        Returns:
            Application result
        """


class DetectionResult(Result[K, E]):
    """Define DetectionResult by subclassing Result."""


__all__ = [
    "Detection", "DetectionResult",
    "DetectionException"
]

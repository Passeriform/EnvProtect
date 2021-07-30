"""Define module-wide exceptions."""
from .crawler import CrawlException
from .dependency import StringParseException
from .detection import DetectionException
from .git import GitignoreNotFoundError
from .report import UnknownOutputStreamError
from .rulebook import RuleSetNotFoundError

__all__ = [
    "CrawlException",
    "StringParseException",
    "DetectionException",
    "GitignoreNotFoundError",
    "UnknownOutputStreamError",
    "RuleSetNotFoundError",
]

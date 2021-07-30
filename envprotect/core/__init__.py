"""Define core modules and operations."""
from .crawler import Crawler, CrawlResult, CrawlException
from .dependency import DependencyBase, DependencyFileType,     \
                        dependency_file_type_mapping,           \
                        fetch_dependencies, parse_dependencies
from .detection import Detection, DetectionResult, DetectionException
from .result import Result, ResultType

__all__ = [
    "Crawler", "CrawlResult", "CrawlException",
    "DependencyBase", "DependencyFileType", "dependency_file_type_mapping", "fetch_dependencies", "parse_dependencies",
    "Detection", "DetectionResult", "DetectionException",
    "Result", "ResultType",
]

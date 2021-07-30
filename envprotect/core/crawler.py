"""Define a crawler module.

Crawls across the files of the repo and executes sequential tasks.
"""

from os import PathLike
from typing import List, Union, Iterator, TypeVar, Any
from git import Repo, Blob
from envprotect.exception.crawler import CrawlException
from envprotect.rulebook import RuleSet
from .detection import DetectionResult, DetectionException
from .result import Result, ResultType

# pylint: disable=invalid-name
K = TypeVar('K', bound=Union[ResultType, Any])
E = TypeVar('E', bound=CrawlException)
# pylint: enable=invalid-name


class CrawlResult(Result[K, E]):
    """Subclass Result for Crawler."""


class Crawler():
    """Standardize crawling over files in repository and applying operation."""

    def __init__(self, source: Union[Repo, PathLike[str]]) -> None:
        """Initialize new crawler object.

        Args:
            source: Repo object or os path signifying root of repository.
        """
        self.source: Union[Repo, PathLike[str]] = source
        self.files: Iterator[Blob]

        if isinstance(self.source, Repo):
            self.files = self.source.tree().traverse()
        else:
            # TODO: Implment a file-crawl system
            self.files = iter(())

    def crawl_and_detect(self,
                         rulesets: List[RuleSet],
                         dry_run: bool = False) -> CrawlResult[List[DetectionResult], CrawlException]:
        """Crawl and perform non-mutation detections.

        Crawl over files of a repository in an iterator, perform detections and
        collect ordered detection results.

        Args:
            rulesets: List of ruleset objects.
            dry_run: Flag for turning on mutation for detection.

        Returns:
            Packed list of exceptions raised while crawling.
        """
        crawls: List[DetectionResult] = []
        crawl_exception: List[CrawlException] = []

        while iter_file := next(self.files):
            try:
                file_data = iter_file.data_stream.read()
                crawls.extend(
                    [ruleset.detect_secrets(target=file_data, apply=not dry_run) for ruleset in rulesets]
                )

            except DetectionException as exception:
                crawl_exception.append(CrawlException(from_exc=exception))

        return CrawlResult(ok=crawls, exception=crawl_exception if crawl_exception != [] else None)


__all__ = [
    "Crawler", "CrawlResult",
    "CrawlException"
]

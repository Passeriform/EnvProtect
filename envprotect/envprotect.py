"""envProtect static code analyzer and secret protection suite.

A utility to automatically parse your project and shift secrets to environment
variables. Provides a cli utility to work through the process and exposes the
core module to provide modifiability.
"""

import os
import re
import traceback
from typing import List, Dict, Any
from pathlib import Path
from os import PathLike
from setuptools.namespaces import flatten
from git import Repo
from git.exc import InvalidGitRepositoryError
from .core.crawler import Crawler, CrawlResult, CrawlException
from .core.dependency import DependencyFileType, DependencyBase, parse_dependencies
from .core.detection import Detection, DetectionResult, DetectionException
from .exception import GitignoreNotFoundError
from .printer.report import Report, RunType
from .rulebook import RuleFactory, RuleSet, RULESET_DEPS_MAP
from .server import fetch_vulnerables


def inspect_gitignore(repo: Repo) -> None:
    """Verify gitignore rules.

    Verify if gitignore contains rule for '.env' files. If not, prompt to
    create a proposed gitignore for later operations.

    Args:
        repo: Git repository object to be worked on.

    Raises:
        OSError: Raises an exception when file opening is inaccessible.
    """
    work_dir: PathLike[str] = os.path.dirname(repo.git_dir)
    gitignore_path = os.path.join(work_dir, '.gitignore')

    if not os.path.isfile(gitignore_path):
        try:
            raise GitignoreNotFoundError(message="""
We couldn't find a valid gitignore for the project.\n\r
We'll make a new one for you. Make sure to update it using a
best practice gitignore template platform
like https://gitignore.io
            """)
        except GitignoreNotFoundError:
            try:
                open(gitignore_path, "w").close()
            except OSError as exception:
                raise exception

    with open(gitignore_path, 'r') as gitignore:
        if any(re.findall(r'.*\.env', line) for line in gitignore):
            return

        new_gitignore_path = os.path.join(work_dir, '.gitignore-proposed')

        with open(new_gitignore_path, "a+") as proposed_gitignore:
            proposed_gitignore.write(str(gitignore))
            proposed_gitignore.write(
                """
# Created by envProtect
# ("https://github.com/Passeriform/envProtect")
.env
                """
            )

        print("""
No entries for .env files were found. We have added a proposed gitignore with
.env and other important ignore rules which can be removed after the dump
operation.

In most scenarios, you can directly replace your existing gitignore with the
proposed one, however we advise to be cautious doing this operation.
        """)


def get_suspected_dependencies(repo: Repo) -> Dict[DependencyFileType, List[DependencyBase]]:
    """Get list of dependencies with known vulnerable key strings.

    Gets dependency objects for all dependencies in the repository and returns
    a list of suspected vulnerable dependencies.

    Args:
        repo: Git repository object to be worked on.

    Returns:
        Dependencies with known vulnerabilities.
    """
    dependency_dict: Dict[DependencyFileType, List[DependencyBase]] = parse_dependencies(repo)

    vulnerable_deps_dict: Dict[DependencyFileType, List[DependencyBase]] = fetch_vulnerables(
        dep_types=dependency_dict.keys()
    )

    suspected_deps_dict: Dict[DependencyFileType, List[DependencyBase]] = {
        file_type: list(filter(
            lambda dependency: dependency in vulnerable_deps_dict[file_type],
            dependencies
        ))
        for (file_type, dependencies) in dependency_dict.items()
    }

    return suspected_deps_dict


def find_repo(path: PathLike[str] = Path(os.getcwd())) -> Repo:
    """Fetch root directory defining git rules.

    Args:
        path: Target path for finding the repo. The search goes up
            directories incrementally.

    Returns:
        Repo object corresponding to target git repository

    Raises:
        InvalidGitRepositoryError: Raised if the search reaches root of filesystem.
    """
    search_dir = path

    # Make this check platform agnostic
    while search_dir != Path('/'):
        try:
            if Repo(search_dir).git_dir:
                return Repo(search_dir)

        except InvalidGitRepositoryError:
            pass

        search_dir = Path(os.path.dirname(search_dir))

    raise InvalidGitRepositoryError("""
This isn't a git repo. Neither does it lie nested within one.
    """)


def scan(allow_dirty: bool = False) -> None:
    """Scan repository for potential security key leaks.

    Scans for gitignore, dependencies and prints the potential leaks. Also allows ability to suppress the false
    positives and apply the changes.

    Args:
        allow_dirty: Flag to proceed with application even if git repository is dirty.
    """
    try:
        # Start by detecting if the working directory is a git repository
        repo: Repo = find_repo()

        if not allow_dirty:
            assert not repo.is_dirty(), """
The repository contains uncommitted changes. No changes were made. To avoid
conflict, please commit/stash your changes or run with --allow-dirty flag.
            """
            return None

        # Verify if gitignore is present and create proposed ignore if not.
        # TODO: Use gitignore_path as modification path later in application stage.
        gitignore_path: PathLike[str] = inspect_gitignore(repo)

        # TODO: Scan additional gitignores and files that resemble secret collection and add them to gitignore-propose
        # more_gitignore = scan_secret_files

        # Inspect and mark dependencies prone to secrets leakage.
        dependencies_dict: Dict[DependencyFileType, List[DependencyBase]] = get_suspected_dependencies(repo)
        flattened_dependencies: List[DependencyBase] = flatten(dependencies_dict.values())

        rulesets: List[RuleSet] = list({
            RuleFactory.fetch_rule_set(RULESET_DEPS_MAP[dependency.name])
            for dependency in flattened_dependencies
        })

        crawler: Crawler = Crawler(source=repo)

        crawl_result: CrawlResult[DetectionResult[Any, DetectionException], CrawlException]

        crawl_result = crawler.crawl_and_detect(
            rulesets=rulesets,
            dry_run=True
        )

        detections: List[Detection]
        (detections, detection_exceptions), crawl_exceptions = crawl_result

        Report.generate(runtype=RunType.DRY_RUN, data=crawl_result).dump(output="stdout")

        print("""
The following secrets were detected in your code. Running this with fixing
operation will write the changes to your repo.

Do you wish to continue fixing the repo (Y/n).
        """)

        if input() == "Y":
            apply_result = [detection.apply() for detection in detections]

            Report.generate(runtype=RunType.Apply, data=apply_result).dump(output="stdout")

    except Exception:
        # Ask to execute in different modes
        traceback.print_exc()

    return None


if __name__ == '__main__':
    # Support 3 scan modes. Manual with tweaks, Automatic with commonly known practices and rigorous with ML
    # TODO: Add Cli parser here
    scan(allow_dirty=True)

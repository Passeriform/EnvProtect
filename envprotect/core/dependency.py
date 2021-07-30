"""Define dependency types and handlers."""

from __future__ import annotations
import os
import re
from os import PathLike
from typing import List, Tuple, Dict, Union, Optional
from enum import Enum
from git import Repo
from envprotect.exception import StringParseException


class DependencyFileType(str, Enum):
    """Enum to represent various types of dependency tree maintainers.

    Takes the form of `<Language>_<One word alias for file type>`
    """

    PY_REQUIREMENTS = 'requirements.txt'
    JS_PACKAGE = 'package.json'
    RB_GEMFILE = 'GEMFILE'


dependency_file_type_mapping = {
    """^(\\w+)(?=[<>!=]*)(.*)$""": DependencyFileType.PY_REQUIREMENTS,
    """^\"(.*?)\\": \\"(.*)\\",$""": DependencyFileType.JS_PACKAGE,
    """^(?:gem ")(.*?)(?:", ")(.*?)(?:")$""": DependencyFileType.RB_GEMFILE
}
"""Dependency format and file type mapping registry."""


class DependencyBase:
    """Define dependency base class.

    Basic dependency class needs to be inherited for specialized dependencies.
    """

    def __init__(self, name: str, version_string: str, source_path: Optional[str] = None) -> None:
        """Initialize new dependency Truebase object.

        Args:
            name: Name alias for dependency.
            version_string: Version string adhering to semver definition (<major>.<minor>.<patch>-<label>)
            source_path: Path of source file containing dependency. Kept for reducing back-referencing.
        """
        self.name = name
        self.version_string = version_string
        self.source_path = source_path

    @classmethod
    def from_string(cls,
                    dep_string: str,
                    file_types: Optional[Union[DependencyFileType, List[DependencyFileType]]] = None,
                    source: Optional[str] = None) -> DependencyBase:
        """Create DependencyBase instance using string.

        Parses string and returns a DependencyBase object.

        Args:
            dep_string: String to parse the dependency object from.
            file_types: File type(s) to be tested for the the passed string.
            source: Path of source file containing dependency. Kept for reducing back-referencing.

        Returns:
            A dependency object extracted from string.
        """
        if file_types is not None:
            if not isinstance(file_types, list):
                file_types = [file_types]
        else:
            file_types = list(dependency_file_type_mapping.values())

        try:
            match_results: List[Tuple[DependencyFileType, re.Match[str]]] = [
                (file_type, match_result)
                for (pattern, file_type)
                in dependency_file_type_mapping.items()
                if file_type in list(
                    set(file_types) & set(dependency_file_type_mapping.values())
                )
                and (match_result := re.fullmatch(pattern, dep_string)) is not None
            ]

            # By default fetch the first match result.
            # Enhance to select the best alternative using ML model
            file_type, match_result = match_results[0]

            name, version_string = match_result.group(1, 2)

        except Exception as exception:
            # TODO: Add fine-tuned exception blocks and custom exceptions
            raise StringParseException(message=f"""
Could not parse string into DependencyBase object. Passed string: {dep_string}
            """) from exception

        return DependencyBase(name=name, version_string=version_string, source_path=source)

    def deserialize_version_string(self) -> Dict[str, Optional[str]]:
        """Create dependency version object from string.

        Returns:
            Dict represented deserialized version string.
        """
        parsed_version = re.search("(\\d+)\\.(\\d+)\\.(\\d+)-(.*)$", self.version_string)

        if parsed_version is None:
            raise Exception(f"Version couldn't be parsed. Version tested was: {self.version_string}")

        parsed_version_dict: Dict[str, Optional[str]] = {
            "major": parsed_version.group(0),
            "minor": parsed_version.group(1),
            "patch": parsed_version.group(2),
            "label": parsed_version.group(3)
        }

        return parsed_version_dict

    @property
    def major(self) -> Optional[str]:
        """Return major release version.

        Returns:
            Major version from version_string.
        """
        return self.deserialize_version_string()["major"]

    @property
    def minor(self) -> Optional[str]:
        """Return minor release version.

        Returns:
            Minor version from version_string.
        """
        return self.deserialize_version_string()["minor"]

    @property
    def patch(self) -> Optional[str]:
        """Return patch release version.

        Returns:
            Patch version from version_string.
        """
        return self.deserialize_version_string()["patch"]

    @property
    def label(self) -> Optional[str]:
        """Return label name.

        Returns:
            Label name from version_string.
        """
        return self.deserialize_version_string()["label"]


def fetch_dependencies(path: str, file_type: Optional[DependencyFileType] = None) -> List[DependencyBase]:
    """Fetch dependencies from a dependency file.

    Args:
        path: Path of the dependency file.
        file_type (Optional): Dependency file type.

    Returns:
        A list of dependency objects.
    """
    with open(path, "r") as file:
        dep_list: List[DependencyBase] = [
            DependencyBase.from_string(file_types=file_type, dep_string=dep_str, source=path)
            for dep_str
            in open(path, "r").readlines()
        ]

        file.close()

        return dep_list


def parse_dependencies(repo: Repo) -> Dict[DependencyFileType, List[DependencyBase]]:
    """Parse dependency and return hash of dependencies.

    Parses dependency files of all types in the working directory and returns
    a dictionary of deserialized dependencies.

    Args:
        repo: Git repo instance for fetching configs and performing
        git operations.

    Returns:
        A dependency file to dependency list dictionry
    """
    work_dir: PathLike[str] = os.path.dirname(repo.git_dir)

    dependency_dict: Dict[DependencyFileType, List[DependencyBase]] = {
        file_type: fetch_dependencies(
            file_type=file_type,
            path=os.path.join(work_dir, file_type)
        ) for file_type in DependencyFileType
    }

    return dependency_dict

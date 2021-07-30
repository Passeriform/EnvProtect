from git.config import GitConfigParser
from typing import Any

def sm_section(name: Any): ...
def sm_name(section: Any): ...
def mkhead(repo: Any, path: Any): ...
def find_first_remote_branch(remotes: Any, branch_name: Any): ...

class SubmoduleConfigParser(GitConfigParser):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def set_submodule(self, submodule: Any) -> None: ...
    def flush_to_index(self) -> None: ...
    def write(self): ...
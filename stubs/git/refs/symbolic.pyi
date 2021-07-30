from typing import Any, Optional

class SymbolicReference:
    repo: Any = ...
    path: Any = ...
    def __init__(self, repo: Any, path: Any) -> None: ...
    def __eq__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...
    def __hash__(self) -> Any: ...
    @property
    def name(self): ...
    @property
    def abspath(self): ...
    @classmethod
    def dereference_recursive(cls, repo: Any, ref_path: Any): ...
    def set_commit(self, commit: Any, logmsg: Optional[Any] = ...): ...
    def set_object(self, object: Any, logmsg: Optional[Any] = ...): ...
    commit: Any = ...
    object: Any = ...
    def set_reference(self, ref: Any, logmsg: Optional[Any] = ...): ...
    reference: Any = ...
    ref: Any = ...
    def is_valid(self): ...
    @property
    def is_detached(self): ...
    def log(self): ...
    def log_append(self, oldbinsha: Any, message: Any, newbinsha: Optional[Any] = ...): ...
    def log_entry(self, index: Any): ...
    @classmethod
    def to_full_path(cls, path: Any): ...
    @classmethod
    def delete(cls, repo: Any, path: Any) -> None: ...
    @classmethod
    def create(cls, repo: Any, path: Any, reference: str = ..., force: bool = ..., logmsg: Optional[Any] = ...): ...
    def rename(self, new_path: Any, force: bool = ...): ...
    @classmethod
    def iter_items(cls, repo: Any, common_path: Optional[Any] = ...): ...
    @classmethod
    def from_path(cls, repo: Any, path: Any): ...
    def is_remote(self): ...

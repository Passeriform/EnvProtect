from .reference import Reference
from typing import Any, Optional

class TagReference(Reference):
    @property
    def commit(self): ...
    @property
    def tag(self): ...
    object: Any = ...
    @classmethod
    def create(cls, repo: Any, path: Any, ref: str = ..., message: Optional[Any] = ..., force: bool = ..., **kwargs: Any): ...
    @classmethod
    def delete(cls, repo: Any, *tags: Any) -> None: ...
Tag = TagReference

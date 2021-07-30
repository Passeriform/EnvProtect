from .head import Head
from typing import Any, Optional

class RemoteReference(Head):
    @classmethod
    def iter_items(cls, repo: Any, common_path: Optional[Any] = ..., remote: Optional[Any] = ...): ...
    @classmethod
    def delete(cls, repo: Any, *refs: Any, **kwargs: Any) -> None: ...
    @classmethod
    def create(cls, *args: Any, **kwargs: Any) -> None: ...

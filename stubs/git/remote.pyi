from git.util import Iterable, LazyMixin, RemoteProgress as RemoteProgress
from typing import Any, Optional

class PushInfo:
    NEW_TAG: Any = ...
    NEW_HEAD: Any = ...
    NO_MATCH: Any = ...
    REJECTED: Any = ...
    REMOTE_REJECTED: Any = ...
    REMOTE_FAILURE: Any = ...
    DELETED: Any = ...
    FORCED_UPDATE: Any = ...
    FAST_FORWARD: Any = ...
    UP_TO_DATE: Any = ...
    ERROR: Any = ...
    flags: Any = ...
    local_ref: Any = ...
    remote_ref_string: Any = ...
    summary: Any = ...
    def __init__(self, flags: Any, local_ref: Any, remote_ref_string: Any, remote: Any, old_commit: Optional[Any] = ..., summary: str = ...) -> None: ...
    @property
    def old_commit(self): ...
    @property
    def remote_ref(self): ...

class FetchInfo:
    NEW_TAG: Any = ...
    NEW_HEAD: Any = ...
    HEAD_UPTODATE: Any = ...
    TAG_UPDATE: Any = ...
    REJECTED: Any = ...
    FORCED_UPDATE: Any = ...
    FAST_FORWARD: Any = ...
    ERROR: Any = ...
    @classmethod
    def refresh(cls): ...
    ref: Any = ...
    flags: Any = ...
    note: Any = ...
    old_commit: Any = ...
    remote_ref_path: Any = ...
    def __init__(self, ref: Any, flags: Any, note: str = ..., old_commit: Optional[Any] = ..., remote_ref_path: Optional[Any] = ...) -> None: ...
    @property
    def name(self): ...
    @property
    def commit(self): ...

class Remote(LazyMixin, Iterable):
    repo: Any = ...
    name: Any = ...
    def __init__(self, repo: Any, name: Any) -> None: ...
    def __getattr__(self, attr: Any): ...
    def __eq__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...
    def __hash__(self) -> Any: ...
    def exists(self): ...
    @classmethod
    def iter_items(cls, repo: Any) -> None: ...
    def set_url(self, new_url: Any, old_url: Optional[Any] = ..., **kwargs: Any): ...
    def add_url(self, url: Any, **kwargs: Any): ...
    def delete_url(self, url: Any, **kwargs: Any): ...
    @property
    def urls(self) -> None: ...
    @property
    def refs(self): ...
    @property
    def stale_refs(self): ...
    @classmethod
    def create(cls, repo: Any, name: Any, url: Any, **kwargs: Any): ...
    add: Any = ...
    @classmethod
    def remove(cls, repo: Any, name: Any): ...
    rm: Any = ...
    def rename(self, new_name: Any): ...
    def update(self, **kwargs: Any): ...
    def fetch(self, refspec: Optional[Any] = ..., progress: Optional[Any] = ..., verbose: bool = ..., **kwargs: Any): ...
    def pull(self, refspec: Optional[Any] = ..., progress: Optional[Any] = ..., **kwargs: Any): ...
    def push(self, refspec: Optional[Any] = ..., progress: Optional[Any] = ..., **kwargs: Any): ...
    @property
    def config_reader(self): ...
    @property
    def config_writer(self): ...

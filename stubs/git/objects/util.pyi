from datetime import tzinfo
from git.util import Actor as Actor
from typing import Any, Optional

def get_object_type_by_name(object_type_name: Any): ...
def utctz_to_altz(utctz: Any): ...
def altz_to_utctz_str(altz: Any): ...
def verify_utctz(offset: Any): ...

class tzoffset(tzinfo):
    def __init__(self, secs_west_of_utc: Any, name: Optional[Any] = ...) -> None: ...
    def __reduce__(self): ...
    def utcoffset(self, dt: Any): ...
    def tzname(self, dt: Any): ...
    def dst(self, dt: Any): ...

utc: Any

def parse_date(string_date: Any): ...
def parse_actor_and_date(line: Any): ...

class ProcessStreamAdapter:
    def __init__(self, process: Any, stream_name: Any) -> None: ...
    def __getattr__(self, attr: Any): ...

class Traversable:
    def list_traverse(self, *args: Any, **kwargs: Any): ...
    def traverse(self, predicate: Any = ..., prune: Any = ..., depth: int = ..., branch_first: bool = ..., visit_once: bool = ..., ignore_self: int = ..., as_edge: bool = ...): ...

class Serializable: ...

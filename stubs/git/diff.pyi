from typing import Any, Optional

NULL_TREE: Any

class Diffable:
    class Index: ...
    def diff(self, other: Any = ..., paths: Optional[Any] = ..., create_patch: bool = ..., **kwargs: Any): ...

class DiffIndex(list):
    change_type: Any = ...
    def iter_change_type(self, change_type: Any) -> None: ...

class Diff:
    re_header: Any = ...
    NULL_HEX_SHA: Any = ...
    NULL_BIN_SHA: Any = ...
    a_mode: Any = ...
    b_mode: Any = ...
    a_rawpath: Any = ...
    b_rawpath: Any = ...
    a_blob: Any = ...
    b_blob: Any = ...
    new_file: Any = ...
    deleted_file: Any = ...
    copied_file: Any = ...
    raw_rename_from: Any = ...
    raw_rename_to: Any = ...
    diff: Any = ...
    change_type: Any = ...
    score: Any = ...
    def __init__(self, repo: Any, a_rawpath: Any, b_rawpath: Any, a_blob_id: Any, b_blob_id: Any, a_mode: Any, b_mode: Any, new_file: Any, deleted_file: Any, copied_file: Any, raw_rename_from: Any, raw_rename_to: Any, diff: Any, change_type: Any, score: Any) -> None: ...
    def __eq__(self, other: Any) -> Any: ...
    def __ne__(self, other: Any) -> Any: ...
    def __hash__(self) -> Any: ...
    @property
    def a_path(self): ...
    @property
    def b_path(self): ...
    @property
    def rename_from(self): ...
    @property
    def rename_to(self): ...
    @property
    def renamed(self): ...
    @property
    def renamed_file(self): ...

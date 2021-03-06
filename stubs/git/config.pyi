import abc
from collections import OrderedDict
from typing import Any, Optional

class MetaParserBuilder(abc.ABCMeta):
    def __new__(cls, name: Any, bases: Any, clsdict: Any): ...

class SectionConstraint:
    def __init__(self, config: Any, section: Any) -> None: ...
    def __del__(self) -> None: ...
    def __getattr__(self, attr: Any): ...
    @property
    def config(self): ...
    def release(self): ...
    def __enter__(self): ...
    def __exit__(self, exception_type: Any, exception_value: Any, traceback: Any) -> None: ...

class _OMD(OrderedDict):
    def __setitem__(self, key: Any, value: Any) -> None: ...
    def add(self, key: Any, value: Any) -> None: ...
    def setall(self, key: Any, values: Any) -> None: ...
    def __getitem__(self, key: Any): ...
    def getlast(self, key: Any): ...
    def setlast(self, key: Any, value: Any) -> None: ...
    def get(self, key: Any, default: Optional[Any] = ...): ...
    def getall(self, key: Any): ...
    def items(self): ...
    def items_all(self): ...

class GitConfigParser:
    t_lock: Any = ...
    re_comment: Any = ...
    optvalueonly_source: str = ...
    OPTVALUEONLY: Any = ...
    OPTCRE: Any = ...
    def __init__(self, file_or_files: Optional[Any] = ..., read_only: bool = ..., merge_includes: bool = ..., config_level: Optional[Any] = ..., repo: Optional[Any] = ...) -> None: ...
    def __del__(self) -> None: ...
    def __enter__(self): ...
    def __exit__(self, exception_type: Any, exception_value: Any, traceback: Any) -> None: ...
    def release(self) -> None: ...
    def optionxform(self, optionstr: Any): ...
    def read(self) -> None: ...
    def items(self, section_name: Any): ...
    def items_all(self, section_name: Any): ...
    def write(self) -> None: ...
    def add_section(self, section: Any): ...
    @property
    def read_only(self): ...
    def get_value(self, section: Any, option: Any, default: Optional[Any] = ...): ...
    def get_values(self, section: Any, option: Any, default: Optional[Any] = ...): ...
    def set_value(self, section: Any, option: Any, value: Any): ...
    def add_value(self, section: Any, option: Any, value: Any): ...
    def rename_section(self, section: Any, new_name: Any): ...

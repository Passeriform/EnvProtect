from gitdb.utils.encoding import force_bytes as force_bytes, force_text as force_text
from typing import Any

is_win: Any
is_posix: Any
is_darwin: Any
defenc: Any

def safe_decode(s: Any): ...
def safe_encode(s: Any): ...
def win_encode(s: Any): ...
def with_metaclass(meta: Any, *bases: Any): ...

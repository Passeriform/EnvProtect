from . import base

class Blob(base.IndexObject):
    DEFAULT_MIME_TYPE: str = ...
    type: str = ...
    executable_mode: int = ...
    file_mode: int = ...
    link_mode: int = ...
    @property
    def mime_type(self): ...

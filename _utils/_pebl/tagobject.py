from typing import Any as _Any
from typing import Optional as _Optional

from lynq.pebl.app import AppObject as _AppObject

class TagObject(_AppObject):
    def __init__(self, name: str, tag: str, args: _Optional[str] = None) -> None:
        super().__init__(name)

        self.tagstr: str = tag

        self.singular(f"<{self.tagstr} {args or ""}>")

    def __exit__(self, *_) -> None:
        self.singular(f"</{self.tagstr}>")
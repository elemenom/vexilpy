from typing import Any
from typing import Optional

from lynq._backendutils.pebl.appobject import AppObject

class TagObject(AppObject):
    def __init__(self, name: str, tag: str, args: Optional[str] = None) -> None:
        super().__init__(name)

        self.tagstr: str = tag

        self.singular(f"<{self.tagstr} {args or ""}>")

    def __exit__(self, *_) -> None:
        self.singular(f"</{self.tagstr}>")
from typing import Any, Optional

from lynq.logger import logger
from lynq.pebl.app import PeblApp

class TagObject(PeblApp):
    def __init__(self, name: str, tag: str, args: Optional[str] = None) -> None:
        super().__init__(name)

        self.tagstr: str = tag

        self.single(f"<{self.tagstr} {args or ""}>")

    def __exit__(self, *_) -> None:
        self.single(f"</{self.tagstr}>")
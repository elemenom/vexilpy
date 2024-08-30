from typing import Optional
from typing import Callable

from lynq._backendutils.lynq.lynqserverorrelated import LynqServerOrRelatedObjects
from lynq.launcher import launch

from lynq._backendutils.pebl.supportswith import SupportsWithKeyword
from lynq._backendutils.pebl.supportedtags import supported_tags

from lynq._backendutils.pebl.blankslateobject import new

class app(SupportsWithKeyword):
    def __init__(self, server: Optional[LynqServerOrRelatedObjects] = None) -> None:
        super().__init__()

        self.server: Optional[LynqServerOrRelatedObjects] = server

        self._init_root()

    def _init_root(self) -> None:
        self.export = new("export", (), # Export types here:
            standard = self._standard
        )

    def _standard(self, fn: Callable) -> Callable:
        self.fn: Callable = fn

        from lynq._backendutils.pebl.saeo import StandardAppExportObject

        return lambda *args, **kwargs: StandardAppExportObject(self, *args, **kwargs)
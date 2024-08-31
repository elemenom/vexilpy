"""
This file is part of Lynq (elemenom/lynq).

Lynq is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lynq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lynq. If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Optional
from typing import Callable

from lynq._backendutils.lynq.lynqserverorrelated import LynqServerOrRelatedObjects
from lynq._backendutils.app.appobject import AppObject
from lynq._backendutils.app.supportswith import SupportsWithKeyword
from lynq._backendutils.app.blankslateobject import new

class app(SupportsWithKeyword):
    def __init__(self, server: Optional[LynqServerOrRelatedObjects] = None) -> None:
        super().__init__()

        self.server: Optional[LynqServerOrRelatedObjects] = server

        self._init_root()

    def _init_root(self) -> None:
        self.export = new("export", (), # Export methods here:
            standard = self.export_standard,
            null = self.export_null,
            direct = self.export_direct,
            dontpass = self.export_nopass
        )

    def export_standard(self, fn: Callable) -> Callable:
        self.fn: Callable = fn

        from lynq._backendutils.app.standardappexportobject import StandardAppExportObject

        return lambda *args, **kwargs: StandardAppExportObject(self, *args, object_=AppObject, **kwargs)
    
    def export_null(self, fn: Callable) -> Callable:
        return lambda *args, **kwargs: fn(*args, **kwargs)
    
    def export_direct(self, fn: Callable) -> None:
        app: AppObject = AppObject(fn.__name__, self.app.server)
        try: return fn(app, *self.args, **self.kwargs)
        finally: app.pass_to_server()
    
    def export_nopass(self, fn: Callable) -> None:
        app: AppObject = AppObject(self.app.fn.__name__, self.app.server)
        return self.app.fn(app, *self.args, **self.kwargs)
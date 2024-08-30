from typing import Callable
from typing import Optional
from typing import Any

from lynq._backendutils.pebl.appobject import AppObject
from lynq.app import app

from lynq.server import BasinLynqServer

class basinapp(app):
    def __init__(self, path: Optional[str] = None) -> None:
        super().__init__(BasinLynqServer(path))
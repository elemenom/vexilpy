from typing import Callable as _Callable
from typing import Any as _Any

from lynq.pebl.app import AppObject as _AppObject
from lynq.pebl.app import app as _app

from lynq.server.basin import BasinLynqServer as _BasinLynqServer

def basinapp(path: str | None = None) -> _Callable:
    return _app(_BasinLynqServer(path))
from typing import Any as _Any

from lynq._basin.object import BasinObject as _BasinObject

def getval(key: str, basin: _BasinObject | None = None, path: str | None = None) -> _Any:
    return (basin or _BasinObject(path)).read_whole()[key]
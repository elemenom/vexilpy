from typing import Any

from lynq._dependencies.basin.object import BasinObject

def getval(key: str, basin: BasinObject | None = None, path: str | None = None) -> Any:
    return (basin or BasinObject(path)).read_whole()[key]
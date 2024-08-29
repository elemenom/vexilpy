from typing import Self as _Self
from typing import Any as _Any

type _BasinReturnObject = dict[str, _Any]

class BasinObject:
    def __init__(self, path: str | None = None) -> None:
        self.path: str = path or "config.bsn"

    def set_path(self, path: str | None = None) -> _Self:
        self.path = path or "config.bsn"

        return self
    
    def read_whole(self) -> _BasinReturnObject:
        o: _BasinReturnObject = {}

        with open(self.path) as file:
            for ln in [i.strip() for i in file.read().split("\n")]:
                print(file.read())
                k, v = ln.strip().split("=", 1)

                o.update({k.strip(): eval(v.strip())})

        return o
    
    def read_line(self, number: int) -> _BasinReturnObject:
        with open(self.path) as file:
            c: str = file.readline(number).strip()
            return {c[0]: eval(c[1])}
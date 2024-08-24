from typing import Self, Any

type BasinReturnObject = dict[str, Any]

class BasinObject:
    def __init__(self, path: str | None = None) -> None:
        self.path: str = path or "config.bsn"

    def set_path(self, path: str | None = None) -> Self:
        self.path = path or "config.bsn"

        return self
    
    def read_whole(self) -> BasinReturnObject:
        o: BasinReturnObject = {}

        with open(self.path) as file:
            for ln in [i.strip() for i in file.readlines()]:
                k, v = ln.split("=", 1)

                o.update({k: eval(v)})

        return o
    
    def read_line(self, number: int) -> BasinReturnObject:
        with open(self.path) as file:
            c: str = file.readline(number).strip()
            return {c[0]: eval(c[1])}
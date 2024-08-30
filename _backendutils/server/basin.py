from lynq.server import LynqServer
from lynq._dependencies.basin.object import BasinObject
from lynq._dependencies.basin.getval import getval

class BasinLynqServer(LynqServer):
    def __init__(self, name: str) -> None:
        from lynq.launcher import launch

        basin: BasinObject = BasinObject(name)

        super().__init__(
            port=getval("port", basin),
            directory=getval("directory", basin)
        )
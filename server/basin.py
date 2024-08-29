"""
The resources in this file will help you connect Basin with
Lynq for Python.

Lynq can use Basin's key-value syntax to create a server from with
custom properties.
"""

from lynq.server.standard import LynqServer
from lynq._basin.object import BasinObject
from lynq._basin.getval import getval

class BasinLynqServer(LynqServer):
    def __init__(self, name: str) -> None:
        from lynq.launcher import launch

        basin: BasinObject = BasinObject(name)

        super().__init__(
            port=getval("port", basin),
            directory=getval("directory", basin)
        )
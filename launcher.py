from typing import Optional as _Optional
from typing import Callable as _Callable

from lynq._utils._lynq.lynqserverorrelated import LynqServerOrRelatedObjects as _LynqServerOrRelatedObjects
from lynq.server.standard import LynqServer as _LynqServer
from lynq.server.custom import ConfigurableLynqServer as _ConfigurableLynqServer

def launch(server: _LynqServerOrRelatedObjects) -> _LynqServerOrRelatedObjects:
    try:
        server.open()
        input("\033[1;93mPress enter to exit your Lynq server...\n\033[0m")

    finally:
        server.close()

        return server

def directlaunch(port: _Optional[int] = None, directory: _Optional[str] = None) -> _LynqServer:
    server: _LynqServer = _LynqServer(port or 8000, directory or ".")

    return launch(server)

def shallow(launch_method: _Callable) -> None:
    server: _LynqServerOrRelatedObjects = launch_method()

    
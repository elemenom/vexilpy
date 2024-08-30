from typing import Optional

from lynq._backendutils.server.standard import LynqServer
from lynq._backendutils.launcher.launch import launch

def directlaunch(port: Optional[int] = None, directory: Optional[str] = None) -> LynqServer:
    server: LynqServer = LynqServer(port or 8000, directory or ".")

    return launch(server)
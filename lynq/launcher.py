from typing import Optional

from lynq.server import LynqServer
from lynq.customserver import ConfigurableLynqServer

def directlaunch(port: Optional[int] = None, directory: Optional[str] = None) -> None:
    server: LynqServer = LynqServer(port or 8000, directory or ".")

    try:
        server.open()
        input("\033[1;93mPress enter to exit your Lynq server...\n\033[0m")

    finally:
        server.close()

def launch(server: LynqServer | ConfigurableLynqServer):
    try:
        server.open()
        input("\033[1;93mPress enter to exit your Lynq server...\n\033[0m")

    finally:
        server.close()
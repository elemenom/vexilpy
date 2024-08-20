from typing import Any, Callable, Optional, Union
import os

from lynq.server import LynqServer
from lynq.logger import logger
from lynq.customserver import ConfigurableLynqServer
from lynq.launcher import launch

from lynq.pebl.supportswith import SupportsWithKeyword

class PeblApp(SupportsWithKeyword):
    def __init__(self, name: str, server: LynqServer | ConfigurableLynqServer | None = None) -> None:

        self.server: Any = server
        self.name: str = f"{name}.html"

    def tag(self, type_: str, args: Optional[str] = None) -> Any:
        from lynq.pebl.tagobject import TagObject

        return TagObject(self.name.removesuffix(".html"), type_, args)
    
    def single(self, ln: str) -> None:
        with open(self.name, "a") as file:
            file.write(ln + "\n")
    
    def __exit__(self, *_) -> None:
        self.pass_to_server()
    
    def pass_to_server(self) -> None:
        if self.server is None:
            logger.error("Cannot pass pebl script to server when no server was provided.")
            raise

        logger.info(f"Passed {self.name} pebl script to {type(self.server).__name__}")

        launch(self.server)

        logger.info("Continuing in pebl app to clear cache.")
        os.remove("index.html")
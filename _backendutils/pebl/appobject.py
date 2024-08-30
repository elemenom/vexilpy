import os

from typing import Optional
from typing import Any

from lynq import GLOBAL_LOGGER as logger

from lynq.launcher import launch

from lynq._backendutils.pebl.supportswith import SupportsWithKeyword
from lynq._backendutils.lynq.lynqserverorrelated import LynqServerOrRelatedObjects
from lynq._backendutils.pebl.supportedtags import supported_tags

class AppObject(SupportsWithKeyword):
    def __init__(self, name: Optional[str], server: Optional[LynqServerOrRelatedObjects] = None) -> None:

        self.server: Any = server
        self.name: str = f"{name}.html"

        self.init_supported_tags(supported_tags)

        self.singular("<!DOCTYPE html>")
        self.singular("<html>")

    def init_supported_tags(self, supported_tags: list[str]) -> None:
        for tag in supported_tags:
            exec(f"self.{tag} = lambda args=None: self.tag({repr(tag)}, args or \"\")", {"self": self})

    def tag(self, type_: str, args: Optional[str] = None) -> Any:
        from lynq._backendutils.pebl.tagobject import TagObject

        return TagObject(self.name.removesuffix(".html"), type_, args)
    
    def singular(self, ln: str) -> None:
        with open(self.name, "a") as file:
            file.write(ln + "\n")
    
    def __exit__(self, *_) -> None:
        self.singular("</html>")

        self.pass_to_server()
    
    def pass_to_server(self) -> None:
        if self.server is None:
            logger.error("Cannot pass pebl script to server when no server was provided.")
            raise

        logger.info(f"Passed {self.name} pebl script to {type(self.server).__name__}")

        launch(self.server)

        logger.info("Continuing in pebl app to clear cache.")
        os.remove("index.html")
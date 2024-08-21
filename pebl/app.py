from typing import Any, Optional, Callable
import os

from lynq.server import LynqServer
from lynq.logger import logger
from lynq.customserver import ConfigurableLynqServer
from lynq.launcher import launch

from lynq.pebl.supportswith import SupportsWithKeyword
from lynq.pebl.supportedtags import supported_tags as supported_tags_

class AppObject(SupportsWithKeyword):
    def __init__(self, name: Optional[str], server: LynqServer | ConfigurableLynqServer | None = None) -> None:

        self.server: Any = server
        self.name: str = f"{name}.html"

        self.init_supported_tags(supported_tags_)

    def init_supported_tags(self, supported_tags: list[str]) -> None:
        for tag in supported_tags:
            exec(f"self.{tag} = lambda args=None: self.tag({repr(tag)}, args or \"\")", {"self": self})

    def tag(self, type_: str, args: Optional[str] = None) -> Any:
        from lynq.pebl.tagobject import TagObject

        return TagObject(self.name.removesuffix(".html"), type_, args)
    
    def singular(self, ln: str) -> None:
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

def appnode(server: LynqServer | ConfigurableLynqServer | None = None) -> Callable:
    def wrapper(fn: Callable) -> Callable:
        def wrapper2(*args: Any, **kwargs: Any) -> Any:
            app: AppObject = AppObject(fn.__name__, server)
            try: return fn(app, *args, **kwargs)
            finally: app.pass_to_server()
        
        return wrapper2
        
    return wrapper
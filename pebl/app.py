from typing import Any as _Any
from typing import Optional as _Optional
from typing import Callable as _Callable
import os as _os

from lynq._utils._lynq.lynqserverorrelated import LynqServerOrRelatedObjects as _LynqServerOrRelatedObjects
from lynq._config import GLOBAL_LOGGER as _logger
from lynq.launcher import launch as _launch

from lynq._utils._pebl.supportswith import SupportsWithKeyword as _SupportsWithKeyword
from lynq._utils._pebl.supportedtags import supported_tags as _supported_tags


class AppObject(_SupportsWithKeyword):
    def __init__(self, name: _Optional[str], server: _LynqServerOrRelatedObjects | None = None) -> None:
        self.server: _Any = server
        self.name: str = f"{name}.html"

        self.init_supported_tags(_supported_tags)

        self.singular("<!DOCTYPE html>")
        self.singular("<html>")

        self.aphtml: bool = auto_prime_html

        self.prime_html() if self.aphtml else None

    def init_supported_tags(self, supported_tags: list[str]) -> None:
        for tag in supported_tags:
            exec(f"self.{tag} = lambda args=None: self.tag({repr(tag)}, args or \"\")", {"self": self})

    def tag(self, type_: str, args: _Optional[str] = None) -> _Any:
        from lynq._utils._pebl.tagobject import TagObject

        return TagObject(self.name.removesuffix(".html"), type_, args)
    
    def singular(self, ln: str) -> None:
        with open(self.name, "a") as file:
            file.write(ln + "\n")
    
    def __exit__(self, *_) -> None:
        self.singular("</html>")

        self.pass_to_server()
    
    def pass_to_server(self) -> None:
        if self.server is None:
            _logger.error("Cannot pass pebl script to server when no server was provided.")
            raise

        _logger.info(f"Passed {self.name} pebl script to {type(self.server).__name__}")

        _launch(self.server)

        _logger.info("Continuing in pebl app to clear cache.")
        _os.remove("index.html")

class app:
    def __init__(self, server: _Optional[_LynqServerOrRelatedObjects] = None) -> None:
        self.server: _Optional[_LynqServerOrRelatedObjects] = server

    def export(self, fn: _Callable) -> _Callable:
        def wrapper(*args: _Any, **kwargs: _Any) -> _Any:
            app_: AppObject = AppObject(fn.__name__, self.server)
              
            try: return fn(app_, *args, **kwargs)
            finally: app_.pass_to_server()
        
        return wrapper
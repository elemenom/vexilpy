"""
This file is part of Lynq (elemenom/lynq).

Lynq is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lynq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lynq. If not, see <https://www.gnu.org/licenses/>.
"""

import os

from typing import Optional
from typing import Any

from lynq import GLOBAL_LOGGER as logger

from lynq._backendutils.launcher.launch import launch

from lynq._backendutils.app.supportswith import SupportsWithKeyword
from lynq._backendutils.lynq.lynqserverorrelated import LynqServerOrRelatedObjects
from lynq._backendutils.app.supportedtags import supported_tags

from lynq._backendutils.style.style import StyledAppAttachment

class AppObject(SupportsWithKeyword):
    def __init__(self, name: Optional[str], app: Any = None) -> None:
        from lynq._backendutils.app.app import app as app_

        self.server: Any = app.server
        self.name: str = f"{name}.html"

        self.app: app_ | None = app

        self.style_: StyledAppAttachment | None = app.style

        self.new_stylesheet_path: str = f"{self.app.fn.__name__}.css"

        self.init_supported_tags(supported_tags)

        self.on_run()

    def on_run(self) -> None:
        logger.info("Please wait while we build your HTML file for you.")

        self.singular("<!DOCTYPE html>")
        self.singular("<html>")
        self.singular(f"<link rel=\"stylesheet\" href=\"{self.new_stylesheet_path}\">")

    def init_supported_tags(self, supported_tags: list[str]) -> None:
        for tag in supported_tags:
            exec(f"self.{tag} = lambda **args: self.tag({repr(tag)}, **args)", {"self": self})

    def tag(self, type_: str, **kwargs: str | int) -> Any:
        from lynq._backendutils.app.tagobject import TagObject

        final_kwargs = ""

        for kwarg in list(kwargs.items()):
            final_kwargs += f"{kwarg[0]}={kwarg[1]} "

        return TagObject(self.name.removesuffix(".html"), type_, self.app, final_kwargs)
    
    def singular(self, ln: str) -> None:
        with open(self.name, "a") as file:
            file.write(ln + "\n")
    
    def __exit__(self, *_) -> None:
        self.singular("</html>")

        logger.info("Building has been finished successfully.")

        self.pass_to_server()
    
    def pass_to_server(self) -> None:
        if self.server is None:
            logger.fatal("Cannot pass pebl script to server when no server was provided.")
            exit(1)

        logger.info(f"Passed '{self.name}' pebl script to host '{type(self.server).__name__}'")

        if self.style is not None:
            logger.info(f"Passed stylesheet '{self.new_stylesheet_path}' to pebl script '{self.name}'.")

            self.style_.close()

        launch(self.server)

        logger.info("Continuing in pebl app to clear cache.")

        try: os.remove(self.name)
        except FileNotFoundError:
            logger.warn(f"Could not find '{self.name}', so it cannot be cleaned.")

        if self.style_ is not None:
            try: os.remove(self.new_stylesheet_path)
            except FileNotFoundError:
                logger.warn(f"Could not find '{self.new_stylesheet_path}', so it cannot be cleaned.")
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

from typing import Optional

from lynq._backendutils.server.standard import LynqServer
from lynq._backendutils.launcher.launch import launch

def directlaunch(port: Optional[int] = None, directory: Optional[str] = None) -> LynqServer:
    server: LynqServer = LynqServer(port or 8000, directory or ".")

    return launch(server)
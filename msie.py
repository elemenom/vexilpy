from subprocess import run
import logging
from typing import Callable as _Callable
from typing import Optional as _Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def pwsh(cmd: str) -> None:
    run(["powershell", "-Command", cmd])

class InternetExplorerInstance:
    def __init__(self) -> None:
        self.pwie: _Callable = lambda cmd: pwsh(f"$ie = New-Object -ComObject \"InternetExplorer.Application\"; {cmd}")

    def open(self) -> None:
        self.pwie("$ie.Visible = $true")
        logger.info("Launched new internet explorer instance")

    def navigate(self, link: _Optional[str]) -> None:
        self.pwie(f"$ie.Navigate({repr(link) or "http://localhost"})")
        logger.info(f"Navigated internet explorer into {link}")

    def refresh(self) -> None:
        self.pwie("$ie.Refresh()")
        logger.info("Refresh internet explorer")
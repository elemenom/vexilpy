from typing import Union

from lynq.server import LynqServer, ConfigurableLynqServer
from lynq.server import BasinLynqServer

type LynqServerOrRelatedObjects = Union[
    LynqServer,
    ConfigurableLynqServer,
    BasinLynqServer

]
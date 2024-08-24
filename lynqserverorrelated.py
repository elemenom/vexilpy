from typing import Union

from lynq.server import LynqServer
from lynq.customserver import ConfigurableLynqServer
from lynq.basinserver import BasinLynqServer

type LynqServerOrRelatedObjects = Union[
    LynqServer,
    ConfigurableLynqServer,
    BasinLynqServer

]
from typing import Union as _Union

from lynq.server.standard import LynqServer as _LynqServer
from lynq.server.custom import ConfigurableLynqServer as _ConfigurableLynqServer
from lynq.server.basin import BasinLynqServer as _BasinLynqServer

type LynqServerOrRelatedObjects = _Union[
    _LynqServer,
    _ConfigurableLynqServer,
    _BasinLynqServer

]
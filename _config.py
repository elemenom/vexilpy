import logging as _logging

from typing import Any as _Any
from typing import Optional as _Optional

_warn: bool = False

try:
    from lynqconfig import LOGGER as _logger # type: ignore
    from lynqconfig import LOGGINGCONFIG as _additional # type: ignore
    from lynqconfig import LOGGINGLEVEL as _level # type: ignore
    from lynqconfig import LOGGINGFORMAT as _format # type: ignore
    from lynqconfig import CLEANPYCACHE as _clean # type: ignore
except ModuleNotFoundError:
    _logger, \
    _additional, \
    _level, \
    _format, \
    _clean \
    = None, None, None, None, None

    _warn = True

_logging.basicConfig(
    level = _level or _logging.DEBUG,
    format = _format or "%(asctime)s ~ %(levelname)s | %(message)s",
    **_additional or {}
)

GLOBAL_LOGGER: _Any = _logger or _logging.getLogger(__name__)
CLEAN_CACHE: bool = _clean or False

if _warn:
    GLOBAL_LOGGER.warning("An error occured while parsing your lynqconfig.py file and all options have been \
returned to their default state/value.")
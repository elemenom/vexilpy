import atexit as _atexit
import os as _os
import logging as _logging

from lynq._utils._lynq.pycache_remover import remove_pycache_from as _remove_pycache_from
from lynq._utils._lynq.pycache_remover import PYCACHE_REMOVAL_LOCATIONS as _pycache_removal_locations

from lynq._config import GLOBAL_LOGGER as _logger
from lynq._config import CLEAN_CACHE as _clean_cache

def _clean_up() -> None:
    handlers: list[_logging.Handler] = _logger.handlers

    _logging.shutdown()

    if _os.path.exists("lynq.log"):
        _os.remove("lynq.log")

def _clean_up_cache() -> None:
    _logger.debug("Commencing pycache clean up process.")

    for path in _pycache_removal_locations:
        _remove_pycache_from(f"./lynq/{path.replace(".", "/")}")

def _at_exit_func() -> None:
    _logger.debug("Commencing clean up process.")
    
    if _clean_cache:
        _clean_up_cache()

    _clean_up()

    print(f"[Exiting...] Program ended successfully. All active servers terminated.")

_atexit.register(_at_exit_func)
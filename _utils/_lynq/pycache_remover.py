import os as _os

from lynq._config import GLOBAL_LOGGER as _logger

PYCACHE_REMOVAL_LOCATIONS: tuple[str] = (
    "",
    "_basin",
    "_utils",
    "_utils._lynq",
    "_utils._pebl",
    "pebl",
    "server"
)

def remove_pycache_from(path: str | None = None) -> None:
    path = f"{path.strip("/")}/__pycache__"

    _logger.debug(f"Now clearing cache in '{path}'")

    try:
        for item in [i for i in _os.listdir(path) if i.endswith(".pyc")]:
            _os.remove(f"{path}/{item}")

        _os.rmdir(path)
    except FileNotFoundError:
        ...
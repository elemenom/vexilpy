import os

PYCACHE_REMOVAL_LOCATIONS: tuple[str] = (
    "",
    "_backendutils",
    "_backendutils.lynq",
    "_backendutils.pebl",
    "_backendutils.server",
    "_backendutils.launcher",
    "_backendutils.basin",
    "_dependencies",
    "_dependencies.basin"
)

def remove_pycache_from(path: str | None = None) -> None:
    from lynq import GLOBAL_LOGGER as logger

    path = f"{path.strip("/")}/__pycache__"

    logger.debug(f"Now clearing cache in '{path}'")

    try:
        for item in [i for i in os.listdir(path) if i.endswith(".pyc")]:
            os.remove(f"{path}/{item}")

        os.rmdir(path)
    except FileNotFoundError:
        logger.warning(f"Could not find cache item in {path}")
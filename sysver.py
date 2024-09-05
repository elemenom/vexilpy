from typing import Final, Any

SYSVER: Final[float] = 8.4

VERSION: Final[dict[str, float | int]] = {
    "whole": SYSVER,
    "major": int(str(SYSVER).split(".")[0]),
    "minor": float(str(SYSVER).split(".")[1]) / 10
}

INSTALL: Final[dict[str, str]] = {
    "pip": "pip install lynq",
    "git": "git clone lynq --branch v9"
}

UPGRADE: Final[dict[str, str]] = {
    "pip": "pip install lynq --upgrade",
    "git": "rm -rf ./*; git clone lynq --branch v9"
}
from typing import Callable
from typing import Any

def new(name: str, superclasses: tuple[Callable, ...], **items: Any) -> Callable:
    return type(name, superclasses, items)
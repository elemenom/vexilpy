from typing import Self as _Self

class SupportsWithKeyword:
    def __init__(self) -> None:
        ...

    def __enter__(self) -> _Self:
        return self
    
    def __exit__(self, *_) -> None:
        ...
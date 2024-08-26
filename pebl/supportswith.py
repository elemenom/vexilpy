from typing import Self

class SupportsWithKeyword:
    def __init__(self) -> None:
        ...

    def __enter__(self) -> Self:
        return self
    
    def __exit__(self, *_) -> None:
        ...
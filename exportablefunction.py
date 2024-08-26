from typing import Callable, Any

class ExportableFunction:
  def __init__(self, fn: Callable, *args: Any, **kwargs: Any) -> None:
    self.fn: Callable = fn
    self.args: tuple[Any, ...] = args
    self.kwargs: dict[str, Any] = kwargs

  def export_with_args_and_return(self, *args: Any, **kwargs: Any) -> Any:
    return self.fn(*args, **kwargs)

  def export_with_args(self, *args: Any, **kwargs: Any) -> None:
    self.fn(*args, **kwargs)

  def export_with_return(self) -> Any:
    return self.fn()

  def export(self) -> None:
    self.fn()

  def export_with_default_args(self) -> None:
    self.fn(*self.args, **self.kwargs)

  def export_with_default_args_and_return(self) -> Any:
    return self.fn(*self.args, **self.kwargs)

  def get(self) -> Callable:
    return self.fn

  def get_blueprint(self, *args: Any, **kwargs: Any) -> (Callable, tuple[Any, ...], dict[str, Any]):
    return (self.fn, args, **kwargs)

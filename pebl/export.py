from lynq.exportablefunction import ExportableFunction

class export:
  def __init__(exp: ExportableFunction, returner: bool = False) -> None:
    self.__r: Any = (exp.export_with_default_args_and_return if returner else exp.export_with_default_args)()

  def get(self) -> Any:
    return self.__r

from typing import Callable, Any

from lynq.pebl.app import AppObject

from lynq.basinserver import BasinLynqServer

def basinappnode(path: str | None = None) -> Callable:
    def wrapper(fn: Callable) -> Callable:
        def wrapper2(*args: Any, **kwargs: Any) -> Any:
            app: AppObject = AppObject(fn.__name__, BasinLynqServer(path))
            try: return fn(app, *args, **kwargs)
            finally: app.pass_to_server()
        
        return wrapper2
        
    return wrapper
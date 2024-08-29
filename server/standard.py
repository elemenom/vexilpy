import http.server as _http
import socketserver as _socketserver
import webbrowser as _webbrowser
import threading as _threading
import logging as _logging
from pathlib import Path as _Path
from typing import Optional as _Optional
from typing import Type as _Type

from lynq._config import GLOBAL_LOGGER as _logger

class LynqServer:
    def __init__(self, port: int, directory: _Optional[str] = None, handler: _Optional[_Type[_http.BaseHTTPRequestHandler]] = None):
        self.port: int = port
        self.directory: _Path = _Path(directory) if directory else _Path.cwd()
        self.handler: _Type[_http.BaseHTTPRequestHandler] = handler or self._create_handler()
        try:
            self.httpd: _socketserver.TCPServer = _socketserver.TCPServer(("localhost", self.port), self.handler)
            self.httpd.directory = str(self.directory)  # Set directory for the server
            _logger.info(f"Server initialized on port {self.port} with directory {self.directory}")
        except OSError as e:
            _logger.error(f"Could not start server on port {self.port}: {e}")
            raise

    def _create_handler(self) -> _Type[_http.BaseHTTPRequestHandler]:
        class CustomHandler(_http.SimpleHTTPRequestHandler):
            def translate_path(self, path: str) -> str:
                # Removes query parameters, etc., from the URL path
                path = path.split('?', 1)[0]
                path = path.split('#', 1)[0]
                path = _Path(path).relative_to('/')

                # Combine the requested path with the server's directory
                full_path = self.server.directory / path

                # Resolve the final absolute path
                return str(full_path.resolve())
        return CustomHandler

    def _start_server(self) -> None:
        server_thread: _threading.Thread = _threading.Thread(target=self.httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        _logger.info(f"Server started on port {self.port}")

    def open(self) -> None:
        self._start_server()
        url = f"http://localhost:{self.port}"
        _logger.info(f"Opening browser at {url}")
        _webbrowser.open(url)

    def _stop_server(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        _logger.info(f"Server on port {self.port} stopped")

    def close(self) -> None:
        self._stop_server()
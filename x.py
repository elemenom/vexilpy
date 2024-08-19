import http.server
import socketserver
import webbrowser
import threading
import logging
from pathlib import Path
from typing import Optional, Type

import json
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LynqServer:
    def __init__(self, port: int, directory: Optional[str] = None, handler: Optional[Type[http.server.BaseHTTPRequestHandler]] = None):
        self.port: int = port
        self.directory: Path = Path(directory) if directory else Path.cwd()
        self.handler: Type[http.server.BaseHTTPRequestHandler] = handler or self._create_handler()
        try:
            self.httpd: socketserver.TCPServer = socketserver.TCPServer(("localhost", self.port), self.handler)
            self.httpd.directory = str(self.directory)  # Set directory for the server
            logger.info(f"Server initialized on port {self.port} with directory {self.directory}")
        except OSError as e:
            logger.error(f"Could not start server on port {self.port}: {e}")
            raise

    def _create_handler(self) -> Type[http.server.BaseHTTPRequestHandler]:
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def translate_path(self, path: str) -> str:
                # Removes query parameters, etc., from the URL path
                path = path.split('?', 1)[0]
                path = path.split('#', 1)[0]
                path = Path(path).relative_to('/')

                # Combine the requested path with the server's directory
                full_path = self.server.directory / path

                # Resolve the final absolute path
                return str(full_path.resolve())
        return CustomHandler

    def _start_server(self) -> None:
        server_thread: threading.Thread = threading.Thread(target=self.httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        logger.info(f"Server started on port {self.port}")

    def open(self) -> None:
        self._start_server()
        url = f"http://localhost:{self.port}"
        logger.info(f"Opening browser at {url}")
        webbrowser.open(url)

    def _stop_server(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        logger.info(f"Server on port {self.port} stopped")

    def close(self) -> None:
        self._stop_server()

logger = logging.getLogger(__name__)

class ConfigurableLynqServer(LynqServer):
    def __init__(self, config_file: Optional[str] = None, directory: Optional[str] = None, handler: Optional[Type[http.server.BaseHTTPRequestHandler]] = None):
        config = self.load_config(config_file)
        port = config.get("port", 8000)  # Default to int
        directory = directory or config.get("directory")
        super().__init__(port, directory, handler)

    @staticmethod
    def load_config(config_file: Optional[str]) -> dict:
        if config_file and Path(config_file).exists():
            with open(config_file, 'r') as f:
                try:
                    config = json.load(f)
                    logger.info(f"Loaded configuration from {config_file}")
                    return config
                except json.JSONDecodeError as e:
                    logger.error(f"Error parsing config file: {e}")
        else:
            logger.warning(f"No valid config file found. Using default settings.")
        return {}

    @staticmethod
    def parse_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Start a local HTTP server.")
        parser.add_argument('--port', type=int, default=8000, help="Port number to run the server on")
        parser.add_argument('--config', type=str, help="Path to configuration file")
        parser.add_argument('--directory', type=str, help="Directory to serve files from")
        return parser.parse_args()
    
def launch(port: Optional[int] = None, directory: Optional[str] = None) -> None:
    server: LynqServer = LynqServer(port or 8000, directory or ".")

    try:
        server.open()
        input("\033[1;93mPress enter to exit your Lynq server...\n\033[0m")

    finally:
        server.close()

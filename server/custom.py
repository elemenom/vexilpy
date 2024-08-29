from typing import Optional as _Optional
from typing import Type as _Type
from pathlib import Path as _Path
import json as _json
import http.server as _http
import argparse as _argparse

from lynq.server.standard import LynqServer as _LynqServer
from lynq._config import GLOBAL_LOGGER as _logger

class ConfigurableLynqServer(_LynqServer):
    def __init__(self, config_file: _Optional[str] = None, directory: _Optional[str] = None, handler: _Optional[_Type[_http.BaseHTTPRequestHandler]] = None):
        config = self.load_config(config_file)
        port = config.get("port", 8000)  # Default to int
        directory = directory or config.get("directory")
        super().__init__(port, directory, handler)

    @staticmethod
    def load_config(config_file: _Optional[str]) -> dict:
        if config_file and _Path(config_file).exists():
            with open(config_file, 'r') as f:
                try:
                    config = _json.load(f)
                    _logger.info(f"Loaded configuration from {config_file}")
                    return config
                except _json.JSONDecodeError as e:
                    _logger.error(f"Error parsing config file: {e}")
        else:
            _logger.warning(f"No valid config file found. Using default settings.")
        return {}

    @staticmethod
    def parse_args() -> _argparse.Namespace:
        parser = _argparse.ArgumentParser(description="Start a local HTTP server.")
        parser.add_argument('--port', type=int, default=8000, help="Port number to run the server on")
        parser.add_argument('--config', type=str, help="Path to configuration file")
        parser.add_argument('--directory', type=str, help="Directory to serve files from")
        return parser.parse_args()
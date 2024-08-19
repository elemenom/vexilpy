# lynq


Lynq for Python is an open-source python framework that allows developers to host servers absurdly easily
(we're talking 1-line easily)
And this isn't even an exaggeration! Once you have Lynq imported, the world is basically in your hands.

Let's look at the most configurable and advanced way to host servers using Lynq,
and move our way down the ladder to the easiest way.

# `ConfigurableLynqServer` Class Documentation

The `ConfigurableLynqServer` class is an extension of the `LynqServer` class that adds flexibility and configurability to the basic HTTP server setup. This class allows the server to be configured either via a JSON configuration file, command-line arguments, or default values. Below is a detailed explanation of its functionality and components.

## Overview

The `ConfigurableLynqServer` class is designed to provide a customizable HTTP server setup by allowing configuration through multiple sources:

1. **Configuration File**: A JSON file containing server settings.
2. **Command-line Arguments**: Options provided via the command line to override or set specific settings.
3. **Default Values**: Fallbacks for when no other configuration is provided.

### Class Definition

```python
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
```

## Constructor: `__init__`

### Parameters

- **`config_file`**: An optional string representing the path to a JSON configuration file. If provided, this file is used to set the server's port and directory.
  
- **`directory`**: An optional string representing the directory from which files will be served. If not provided, it defaults to the directory specified in the configuration file or remains `None`.
  
- **`handler`**: An optional HTTP request handler class. If not specified, a default handler is used.

### Functionality

1. **Load Configuration**: The constructor calls the `load_config` method to load settings from the provided configuration file (if any).

2. **Port Setup**: The server port is determined by checking the loaded configuration for a `"port"` key. If absent, it defaults to `8000`.

3. **Directory Setup**: The directory is set based on the provided argument or from the configuration file if the argument is `None`.

4. **Superclass Initialization**: The constructor calls the superclass (`LynqServer`) constructor with the determined port, directory, and handler.

## Methods

### `load_config(config_file: Optional[str]) -> dict`

#### Description

This static method attempts to load a configuration file in JSON format.

#### Parameters

- **`config_file`**: A string representing the path to the configuration file. It can be `None` if no file is provided.

#### Returns

- A dictionary containing the configuration settings. If the file doesn't exist or can't be parsed, an empty dictionary is returned.

#### Functionality

1. **File Existence Check**: The method checks if the provided configuration file path exists.
  
2. **File Parsing**: If the file exists, it attempts to parse it as JSON. Errors during parsing are logged, and an empty dictionary is returned.
  
3. **Fallback**: If the file doesn't exist or cannot be loaded, a warning is logged, and the method returns an empty dictionary.

### `parse_args() -> argparse.Namespace`

#### Description

This static method parses command-line arguments to provide additional configuration options for the server.

#### Returns

- An `argparse.Namespace` object containing the parsed arguments.

#### Arguments

- **`--port`**: The port number on which the server should run. Defaults to `8000`.
  
- **`--config`**: The path to the configuration file.
  
- **`--directory`**: The directory to serve files from.

#### Usage

This method is typically called when running the server script from the command line, allowing users to override defaults or configuration file settings directly.

## Usage Example

```python
if __name__ == "__main__":
    args = ConfigurableLynqServer.parse_args()
    server = ConfigurableLynqServer(config_file=args.config, directory=args.directory)
    server.serve_forever()
```

In this example:

1. Command-line arguments are parsed.
2. A `ConfigurableLynqServer` instance is created using the parsed arguments.
3. The server is started, serving files from the specified directory and listening on the specified port.

## Summary

The `ConfigurableLynqServer` class offers a flexible way to configure and run an HTTP server. By leveraging configuration files, command-line arguments, and defaults, it provides a robust mechanism to tailor server behavior to various needs.

**`ConfigurableLynqServer` is a great choice for experienced programmers that know what they're doing**

# `LynqServer` Class Documentation

The `LynqServer` class provides a basic, customizable HTTP server capable of serving files from a specified directory. It leverages Python’s `http.server` and `socketserver` modules to handle HTTP requests and manage the server’s lifecycle. Below is a detailed explanation of its functionality and components.

## Overview

The `LynqServer` class is designed to facilitate the creation and management of a simple HTTP server. It provides functionality to:

- Initialize the server with a specific port and directory.
- Create a custom request handler.
- Start and stop the server.
- Automatically open a web browser pointing to the server’s URL.

### Class Definition

```python
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
```

## Constructor: `__init__`

### Parameters

- **`port`**: An integer specifying the port number on which the server will listen.
  
- **`directory`**: An optional string representing the directory from which the server will serve files. If not provided, it defaults to the current working directory (`Path.cwd()`).

- **`handler`**: An optional HTTP request handler class. If not specified, a custom handler is created using the `_create_handler` method.

### Functionality

1. **Port Initialization**: The port is set based on the provided argument.
  
2. **Directory Initialization**: The directory is set to the provided path or defaults to the current working directory.

3. **Request Handler**: The server uses the provided handler or a custom handler created by `_create_handler`.

4. **Server Setup**: The server is initialized with the `socketserver.TCPServer` class, binding it to `localhost` on the specified port and using the configured request handler.

5. **Error Handling**: If the server fails to start (e.g., due to the port being in use), an error is logged, and an `OSError` is raised.

## Methods

### `_create_handler() -> Type[http.server.BaseHTTPRequestHandler]`

#### Description

This private method creates and returns a custom request handler class based on `http.server.SimpleHTTPRequestHandler`.

#### Functionality

- **Path Translation**: The `translate_path` method is overridden to clean the URL path by removing query parameters and fragments. It then combines the cleaned path with the server’s base directory to determine the absolute file path to be served.

### `_start_server() -> None`

#### Description

This private method starts the server in a background thread, allowing it to serve requests indefinitely without blocking the main thread.

#### Functionality

- **Threading**: The server runs in a daemon thread, meaning it will automatically stop when the main program exits.
  
- **Logging**: A message is logged when the server starts successfully.

### `open() -> None`

#### Description

This method starts the server and opens the default web browser to the server's URL.

#### Functionality

- **Start Server**: The server is started using `_start_server`.
  
- **Open Browser**: The server's URL (`http://localhost:{port}`) is opened in the default web browser.

### `_stop_server() -> None`

#### Description

This private method stops the server gracefully by shutting it down and closing the server socket.

#### Functionality

- **Shutdown**: The server's request-handling loop is stopped.
  
- **Close Socket**: The server socket is closed, freeing up the port.
  
- **Logging**: A message is logged indicating that the server has been stopped.

### `close() -> None`

#### Description

This method is a public interface to stop the server by calling `_stop_server`.

#### Functionality

- **Stop Server**: The server is stopped and cleaned up.

## Usage Example

```python
if __name__ == "__main__":
    server = LynqServer(port=8000, directory="/path/to/serve")
    server.open()
    # The server is now running and serving files
    try:
        while True:
            pass  # Keep the main thread alive
    except KeyboardInterrupt:
        server.close()  # Stop the server on Ctrl+C
```

In this example:

1. The server is initialized with a specific port and directory.
2. The server is started, and the default web browser opens to the server's URL.
3. The server runs indefinitely until interrupted (e.g., via `Ctrl+C`), after which it stops gracefully.

## Summary

The `LynqServer` class provides a simple and customizable way to create an HTTP server. With built-in methods for server management and a customizable request handler, it is well-suited for scenarios requiring a lightweight and configurable web server.

**`LynqServer` is a great choice for intermediate programmers that know how this works, but aren't quite experienced enough to tackle `ConfigurableLynqServer`**

# `launch` Function Documentation

The `launch` function is a utility function that simplifies the process of starting a `LynqServer` instance. It is designed to quickly initialize, start, and manage the lifecycle of a basic HTTP server with minimal setup.

## Function Definition

```python
def launch(port: Optional[int] = None, directory: Optional[str] = None) -> None:
    server: LynqServer = LynqServer(port or 8000, directory or ".")

    try:
        server.open()
        input("\033[1;93mPress enter to exit your Lynq server...\n\033[0m")

    finally:
        server.close()
```

### Parameters

- **`port`**: An optional integer specifying the port number on which the server will listen. If not provided, the function defaults to port `8000`.

- **`directory`**: An optional string specifying the directory from which the server will serve files. If not provided, the function defaults to the current directory (`"."`).

### Functionality

1. **Server Initialization**: 
    - The function initializes a `LynqServer` instance using the provided `port` and `directory` arguments. 
    - If either argument is not provided, it falls back to the default values: port `8000` and the current directory (`"."`).

2. **Server Startup**:
    - The `server.open()` method is called to start the server. 
    - This method also opens the default web browser to the server's URL (`http://localhost:{port}`).

3. **User Prompt**:
    - The function waits for user input with a prompt: "Press enter to exit your Lynq server...".
    - The prompt is displayed in yellow text to stand out in the console.

4. **Server Shutdown**:
    - Regardless of how the function exits (either after user input or due to an exception), the server is properly closed by calling `server.close()`.
    - This ensures that the server shuts down gracefully and the port is released.

### Usage Example

```python
if __name__ == "__main__":
    launch(port=8080, directory="/path/to/serve")
```

In this example:

- The `launch` function is called with a specific port (`8080`) and directory (`/path/to/serve`).
- The server starts and serves files from the specified directory.
- The function waits for the user to press enter, after which the server shuts down.

### Summary

The `launch` function provides a convenient way to start and manage a `LynqServer` instance with minimal code. It handles the server’s lifecycle, from initialization to shutdown, and includes user interaction to control when the server should stop running. This makes it an ideal entry point for scripts that need to quickly start a basic HTTP server.

**`launch()` is a great choice for beginners, or basically anybody who just wants to open a server really quickly and efficiently.**

# Summary

*As you saw from the above documentation, Lynq for Python is a quick, efficient web framework that is insanely easy to master, features many different levels of difficulty to appeal to different skill-levels of programmers, and overall is great at it's job; hosting local servers easily, as smooth as butter.*

- All Lynq servers (no matter the type) will run until the heat death of the universe (unless you press enter to exit them manually)

# Lynq x MSIE

You can now host custom instances of internet explorer that very easily allow you to remotely interact with them using their COM objects.

DISCLAIMER: We are *not* partnered with Microsoft or any other company, all material is open source.

# `InternetExplorerInstance` Class Documentation

The `InternetExplorerInstance` class provides a high-level interface for controlling Internet Explorer instances via PowerShell commands. This class allows for launching a new Internet Explorer window, navigating to specific URLs, and refreshing the browser window. It utilizes the PowerShell COM object model to interact with Internet Explorer.

## Overview

The `InternetExplorerInstance` class is designed to facilitate browser automation with Internet Explorer, using PowerShell scripts executed through Python’s `subprocess` module. This class is particularly useful for scripting and testing environments where Internet Explorer is required.

### Class Definition

```python
class InternetExplorerInstance:
    def __init__(self) -> None:
        self.pwie: Callable = lambda cmd: pwsh(f"$ie = New-Object -ComObject \"InternetExplorer.Application\"; {cmd}")

    def open(self) -> None:
        self.pwie("$ie.Visible = $true")
        logger.info("Launched new internet explorer instance")

    def navigate(self, link: Optional[str]) -> None:
        self.pwie(f"$ie.Navigate({repr(link) or 'http://localhost'})")
        logger.info(f"Navigated internet explorer into {link}")

    def refresh(self) -> None:
        self.pwie("$ie.Refresh()")
        logger.info("Refresh internet explorer")
```

## Methods

### `__init__() -> None`

#### Description

The constructor initializes an instance of `InternetExplorerInstance`.

#### Functionality

- **PowerShell Command Wrapper**: Defines a `self.pwie` lambda function to run PowerShell commands that create a new Internet Explorer COM object. This lambda function calls the `pwsh` function with the appropriate PowerShell command string.

### `open() -> None`

#### Description

Launches a new Internet Explorer instance and makes it visible.

#### Functionality

- **PowerShell Command**: Executes a PowerShell command to make the Internet Explorer instance visible.
  
- **Logging**: Logs an informational message indicating that a new Internet Explorer instance has been launched.

### `navigate(link: Optional[str]) -> None`

#### Description

Navigates the Internet Explorer instance to a specified URL.

#### Parameters

- **`link`**: An optional string representing the URL to navigate to. If `None`, it defaults to `http://localhost`.

#### Functionality

- **PowerShell Command**: Executes a PowerShell command to navigate to the specified URL.

- **Logging**: Logs an informational message indicating the URL to which the browser is navigating.

### `refresh() -> None`

#### Description

Refreshes the current page in the Internet Explorer instance.

#### Functionality

- **PowerShell Command**: Executes a PowerShell command to refresh the current page.

- **Logging**: Logs an informational message indicating that the Internet Explorer instance is being refreshed.

## Dependencies

- **PowerShell**: Required to execute PowerShell commands.
- **Internet Explorer**: The class specifically targets Internet Explorer via its COM object model.
- **Python Libraries**: 
  - `subprocess.run`: To execute PowerShell commands from Python.
  - `logging`: To provide logging functionality.

## Example Usage

```python
if __name__ == "__main__":
    ie = InternetExplorerInstance()
    ie.open()  # Launches a new Internet Explorer instance
    ie.navigate("https://www.example.com")  # Navigates to "https://www.example.com"
    ie.refresh()  # Refreshes the current page
```

In this example:

1. An `InternetExplorerInstance` object is created.
2. The `open` method is called to launch a new Internet Explorer window.
3. The `navigate` method is used to direct the browser to a specific URL.
4. The `refresh` method is invoked to refresh the page.

## Summary

The `InternetExplorerInstance` class provides a Python interface to automate Internet Explorer using PowerShell. It supports opening a new browser window, navigating to URLs, and refreshing the page. This class is useful in scenarios where Internet Explorer needs to be controlled programmatically, particularly in testing or automation tasks.

**Microsoft Internet Explorer is deprecated, but it's still a handy tool to view local servers (via localhost), and Lynq let's you do that quickly and easily.**

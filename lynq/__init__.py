import atexit
import os
import logging

from lynq.logger import logger, warn_count

def clean_up() -> None:
    handlers: list[logging.Handler] = logger.handlers

    logging.shutdown()

    if os.path.exists("lynq.log"):
        os.remove("lynq.log")
        print(f"[Exiting...] Program ran successfully >> {warn_count} warning(s) in total")

atexit.register(clean_up)
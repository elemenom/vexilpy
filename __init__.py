import atexit
import os
import logging

from lynq.logger import logger

def clean_up() -> None:
    handlers: list[logging.Handler] = logger.handlers

    logging.shutdown()

    if os.path.exists("lynq.log"):
        os.remove("lynq.log")

def at_exit_func() -> None:
    logger.info("Nearing program end, commencing clean up process.")
    
    clean_up()

    print(f"[Exiting...] Program ended successfully. All active servers terminated.")

atexit.register(at_exit_func)
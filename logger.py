import logging
import subprocess

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s ~ %(levelname)s | %(message)s'
)
logger: logging.Logger = logging.getLogger(__name__)

warn_count: int = 0
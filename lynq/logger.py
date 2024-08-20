import logging
import subprocess

logging.basicConfig(
    filename='lynq.log',
    level=logging.DEBUG,
    format='%(asctime)s ~ %(levelname)s | %(message)s'
)
logger: logging.Logger = logging.getLogger(__name__)

warn_count: int = 0

subprocess.Popen(["start", "cmd", "/K", "type", "lynq.log"], shell=True)
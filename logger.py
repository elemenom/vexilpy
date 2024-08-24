import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s ~ %(levelname)s | %(message)s'
)
logger: logging.Logger = logging.getLogger(__name__)
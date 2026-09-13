import time
from src.utils.logger import get_logger

logger = get_logger(__name__)


def with_retry(func, endpoint: str, max_attempts: int = 3, wait_seconds: int = 5):
    """Calls func up to max_attempts times, waiting between failures."""
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as e:
            last_error = e
            logger.warning(f"Attempt {attempt}/{max_attempts} failed for {endpoint}: {e}")
            if attempt < max_attempts:
                time.sleep(wait_seconds)

    raise last_error
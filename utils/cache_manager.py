"""Robust exponential backoff retry decorator with randomized full jitter.
Created: 2026-11-09T16:43:18Z
"""

import time
import random
import functools
import logging
from typing import Callable, Tuple, Type

logger = logging.getLogger("retry")

def retry_with_backoff(
    retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable:
    """Decorator to retry flaky I/O or network operations."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_err = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_err = e
                    if attempt == retries:
                        logger.error(f"[Retry] Function {func.__name__} failed after {retries} attempts.")
                        raise
                    sleep_time = delay * (1 + random.random()) if jitter else delay
                    logger.warning(f"[Retry] {func.__name__} failed ({e}). Retrying in {sleep_time:.2f}s (Attempt {attempt}/{retries})...")
                    time.sleep(sleep_time)
                    delay *= backoff_factor
            raise last_err
        return wrapper
    return decorator

# Updated timestamp: 2026-11-09T16:43:18Z (iteration 21)

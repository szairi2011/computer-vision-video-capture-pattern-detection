"""Reusable decorators for pipeline operations."""

import time
import functools  # Tools for functional programming (wraps, partial, etc.)
# Callable: Type hint for functions (Callable[[arg_types], return_type])
# Any: Type hint for any type (use sparingly, prefer specific types)
from typing import Callable, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Decorator Pattern: Function that wraps another function to add behavior
# Why: Separates cross-cutting concerns (timing, logging, retry) from business logic
# Usage: @timer above function definition
def timer(func: Callable) -> Callable:  # Takes function, returns wrapped function
    """Decorator to measure execution time."""
    # @functools.wraps: Preserves original function's metadata (__name__, __doc__, etc.)
    # Why: Without this, wrapped function loses its name/docstring (breaks debugging)
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:  # *args = positional args, **kwargs = keyword args
        start = time.time()  # Record start time
        result = func(*args, **kwargs)  # Call original function
        elapsed = time.time() - start  # Calculate duration
        logger.info(f"{func.__name__} executed in {elapsed:.2f}s")
        return result  # Return original result (transparent wrapper)
    return wrapper  # Return wrapper function (replaces original)


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator to retry failed operations."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"{func.__name__} failed (attempt {attempt + 1}/{max_attempts}): {e}")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


def log_execution(func: Callable) -> Callable:
    """Decorator to log function execution."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger.info(f"Executing {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} completed successfully")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} failed: {e}")
            raise
    return wrapper

"""Define helper functions."""

import time
from functools import wraps


def timer(func: object, iterations: int = 1) -> object:
    """Print runtime of decorated function.

    Args:
        func: decorated function
        iterations: times a function will be executed to determine its average run time
    Returns:
        Decorator function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            times = []
            for _ in range(iterations):
                start_time = time.perf_counter()
                result = func(*args, **kwargs)
                times.append(time.perf_counter() - start_time)
            average_run_time = sum(times) / len(times)
            print(
                f"Finished {func.__name__} in {average_run_time:.4f} seconds on average"
            )
            return result
        return wrapper
    return decorator

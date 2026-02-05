import time


def now_unix() -> int:
    """
    Current Unix timestamp (seconds).
    """
    return int(time.time())


def elapsed_seconds(start_ts: int) -> int:
    """
    Compute elapsed seconds from a given start timestamp.
    """
    return max(0, now_unix() - start_ts)

import os
import time
from typing import Dict, Any, Set
import httpx


CALLBACK_URL = os.getenv("CALLBACK_URL")
CALLBACK_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 2


# In-memory idempotency guard (session-level)
_sent_sessions: Set[str] = set()


def send_callback(payload: Dict[str, Any]) -> bool:
    session_id = payload.get("sessionId")
    if not session_id:
        return False

    if session_id in _sent_sessions:
        return True

    success = _attempt_send_with_retry(payload)
    if success:
        _sent_sessions.add(session_id)

    return success


def _attempt_send_with_retry(payload: Dict[str, Any]) -> bool:
    if not CALLBACK_URL:
        return False

    for attempt in range(MAX_RETRIES):
        try:
            response = httpx.post(
                CALLBACK_URL,
                json=payload,
                timeout=CALLBACK_TIMEOUT,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code in (200, 201, 202):
                return True

            if response.status_code >= 500 and attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BACKOFF_BASE ** attempt)
                continue

            return False

        except (httpx.TimeoutException, httpx.RequestError):
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BACKOFF_BASE ** attempt)
                continue
            return False

        except Exception:
            return False

    return False


def has_callback_been_sent(session_id: str) -> bool:
    return session_id in _sent_sessions

from typing import Dict


# In-memory per-session message counters
_message_counters: Dict[str, int] = {}


def increment_message_counter(session_id: str) -> None:
    if session_id not in _message_counters:
        _message_counters[session_id] = 0
    _message_counters[session_id] += 1


def get_message_count(session_id: str) -> int:
    return _message_counters.get(session_id, 0)


def delete_counter(session_id: str) -> None:
    if session_id in _message_counters:
        del _message_counters[session_id]

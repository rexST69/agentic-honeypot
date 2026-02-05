from typing import Dict
from app.core.state_machine import FSMState


# In-memory session state store (opaque)
_sessions: Dict[str, FSMState] = {}


def create_session(session_id: str) -> None:
    if session_id not in _sessions:
        _sessions[session_id] = FSMState.INIT


def session_exists(session_id: str) -> bool:
    return session_id in _sessions


def get_session_state(session_id: str) -> FSMState:
    if session_id not in _sessions:
        create_session(session_id)
    return _sessions[session_id]


def set_session_state(session_id: str, state: FSMState) -> None:
    if session_id not in _sessions:
        create_session(session_id)
    _sessions[session_id] = state


def delete_session(session_id: str) -> None:
    if session_id in _sessions:
        del _sessions[session_id]

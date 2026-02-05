from app.core.state_machine import FSMState
from app.core.orchestrator import (
    transition_to_intel_ready,
    transition_to_callback_sent,
    transition_to_terminated,
)


def finalize_intelligence(current_state: FSMState) -> FSMState:
    """
    Explicit finalization step.
    Moves AGENT_ENGAGED → INTEL_READY only.
    """
    if current_state != FSMState.AGENT_ENGAGED:
        return current_state
    return transition_to_intel_ready(current_state)


def mark_callback_sent(current_state: FSMState) -> FSMState:
    """
    Marks that callback has been successfully sent.
    """
    if current_state != FSMState.INTEL_READY:
        return current_state
    return transition_to_callback_sent(current_state)


def terminate_session(current_state: FSMState) -> FSMState:
    """
    Final termination.
    """
    if current_state != FSMState.CALLBACK_SENT:
        return current_state
    return transition_to_terminated(current_state)

import pytest
from app.core.state_machine import FSMState, TERMINAL_STATES
from app.core.orchestrator import (
    transition_to_normal,
    transition_to_suspicious,
    transition_to_agent_engaged,
    transition_to_intel_ready,
    transition_to_callback_sent,
    transition_to_terminated,
    is_terminal_state,
)


def test_terminal_state_is_final():
    assert FSMState.TERMINATED in TERMINAL_STATES
    assert is_terminal_state(FSMState.TERMINATED)


def test_valid_forward_transitions():
    assert transition_to_normal(FSMState.INIT) == FSMState.NORMAL
    assert transition_to_suspicious(FSMState.NORMAL) == FSMState.SUSPICIOUS
    assert transition_to_agent_engaged(FSMState.SUSPICIOUS) == FSMState.AGENT_ENGAGED
    assert transition_to_intel_ready(FSMState.AGENT_ENGAGED) == FSMState.INTEL_READY
    assert transition_to_callback_sent(FSMState.INTEL_READY) == FSMState.CALLBACK_SENT
    assert transition_to_terminated(FSMState.CALLBACK_SENT) == FSMState.TERMINATED


def test_invalid_transitions_raise():
    with pytest.raises(Exception):
        transition_to_suspicious(FSMState.INIT)

    with pytest.raises(Exception):
        transition_to_agent_engaged(FSMState.NORMAL)

    with pytest.raises(Exception):
        transition_to_intel_ready(FSMState.SUSPICIOUS)

    with pytest.raises(Exception):
        transition_to_callback_sent(FSMState.AGENT_ENGAGED)

    with pytest.raises(Exception):
        transition_to_normal(FSMState.TERMINATED)

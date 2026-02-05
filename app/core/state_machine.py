from enum import Enum


class FSMState(str, Enum):
    """
    Finite State Machine states for the honeypot session lifecycle.

    States are strictly one-way and must follow the defined order.
    This file is declarative only. No transitions are defined here.
    """
    INIT = "INIT"
    NORMAL = "NORMAL"
    SUSPICIOUS = "SUSPICIOUS"
    AGENT_ENGAGED = "AGENT_ENGAGED"
    INTEL_READY = "INTEL_READY"
    CALLBACK_SENT = "CALLBACK_SENT"
    TERMINATED = "TERMINATED"


# Ordered lifecycle definition (authoritative)
VALID_STATE_ORDER = (
    FSMState.INIT,
    FSMState.NORMAL,
    FSMState.SUSPICIOUS,
    FSMState.AGENT_ENGAGED,
    FSMState.INTEL_READY,
    FSMState.CALLBACK_SENT,
    FSMState.TERMINATED,
)


# Ordinal index for monotonic reasoning (read-only use)
STATE_ORDINAL_MAP = {state: idx for idx, state in enumerate(VALID_STATE_ORDER)}


# Terminal states (no further transitions allowed)
TERMINAL_STATES = frozenset({
    FSMState.TERMINATED
})

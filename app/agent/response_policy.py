from enum import Enum, auto
from typing import List


class ResponseCategory(Enum):
    CONFUSION = auto()
    CLARIFICATION = auto()
    HESITATION = auto()
    MILD_CONCERN = auto()
    DELAY_TACTIC = auto()
    PARTIAL_COMPLIANCE = auto()
    MISTAKE_ADMISSION = auto()
    ALTERNATIVE_REQUEST = auto()
    SOFT_FAILURE = auto()


def select_response_category(
    turn_count: int,
    detected_signals: List[str],
    scammer_asking_for_data: bool,
    scammer_showing_urgency: bool,
) -> ResponseCategory:
    """
    Select an abstract response category.
    This function does NOT inspect raw text.
    """
# Intentional soft-failure loop to prolong engagement
    if scammer_asking_for_data and turn_count >= 4 and turn_count % 3 == 1:
        return ResponseCategory.SOFT_FAILURE

    if turn_count <= 2:
        return ResponseCategory.CONFUSION

    if scammer_asking_for_data and turn_count <= 4:
        return ResponseCategory.CLARIFICATION

    if scammer_showing_urgency:
        if turn_count % 3 == 0:
            return ResponseCategory.DELAY_TACTIC
        return ResponseCategory.MILD_CONCERN

    if scammer_asking_for_data and turn_count > 4:
        mod = turn_count % 4
        if mod == 0:
            return ResponseCategory.ALTERNATIVE_REQUEST
        if mod == 1:
            return ResponseCategory.HESITATION
        return ResponseCategory.PARTIAL_COMPLIANCE

    if turn_count > 8 and turn_count % 5 == 0:
        return ResponseCategory.MISTAKE_ADMISSION

    return (
        ResponseCategory.CLARIFICATION
        if turn_count % 2 == 0
        else ResponseCategory.HESITATION
    )


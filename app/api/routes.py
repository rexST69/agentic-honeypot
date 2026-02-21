from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.api.schemas import IncomingRequest, APIResponse
from app.api.auth import verify_api_key

limiter = Limiter(key_func=get_remote_address)

from app.core import session_store, orchestrator, detection
from app.core.state_machine import FSMState
from app.agent import response_policy, llm_client, persona
from app.metrics import counters
from app.extraction import extractor
from app.extraction import store as extraction_store
from app.core.termination import finalize_intelligence, mark_callback_sent, terminate_session
from app.callback.payload_builder import build_callback_payload
from app.callback.sender import send_callback


router = APIRouter()

MIN_TURNS_FOR_FINALIZATION = 6
MIN_INTEL_TYPES = 2


def build_agent_notes(
    session_id: str,
    turn_count: int,
    detection_signals: list,
) -> str:
    intelligence = extraction_store.get_all_intelligence(session_id)
    notes = []

    if "urgency_detected" in detection_signals:
        notes.append("Scammer escalated urgency.")

    if "financial_request" in detection_signals:
        notes.append("Scammer requested financial action.")

    if intelligence.get("upiIds"):
        notes.append("UPI identifier captured.")

    if intelligence.get("phishingLinks"):
        notes.append("Phishing link captured.")

    if intelligence.get("phoneNumbers"):
        notes.append("Phone number captured.")

    notes.append(f"Engaged for {turn_count} turns.")
    return " ".join(notes)


@router.post(
    "/message",
    response_model=APIResponse,
    dependencies=[Depends(verify_api_key)],
)
@limiter.limit("30/minute")
def handle_message(request: Request, body: IncomingRequest) -> APIResponse:
    session_id = body.sessionId
    incoming_text = body.message.text

    # 1. Load or create session
    session_store.create_session(session_id)
    current_state = session_store.get_session_state(session_id)

    # 2. Terminal guard (hard stop, prevents double callback)
    if orchestrator.is_terminal_state(current_state):
        return APIResponse(status="success", reply="Thank you.")

    # 3. Increment metrics
    counters.increment_message_counter(session_id)
    turn_count = counters.get_message_count(session_id)

    # 4. Detection (pure analysis)
    detection_result = detection.analyze_message(incoming_text)

    # 5. FSM transition decision
    next_state = orchestrator.next_state(
        current_state=current_state,
        detection_result=detection_result,
        turn_count=turn_count,
    )

    if next_state != current_state:
        session_store.set_session_state(session_id, next_state)
        current_state = next_state

    # 6. Agent engaged behavior
    if current_state == FSMState.AGENT_ENGAGED:
        extractor.extract_intelligence_from_message(session_id, incoming_text)

        # ---- Finalization gate (routes-level) ----
        intel = extraction_store.get_all_intelligence(session_id)
        intel_type_count = sum(1 for v in intel.values() if v)

        if (
            turn_count >= MIN_TURNS_FOR_FINALIZATION
            and intel_type_count >= MIN_INTEL_TYPES
        ):
            new_state = finalize_intelligence(current_state)
            if new_state != current_state:
                session_store.set_session_state(session_id, new_state)
                current_state = new_state

    # 7. Callback (exactly once)
    if current_state == FSMState.INTEL_READY:
        intelligence = extraction_store.get_all_intelligence(session_id)

        agent_notes = build_agent_notes(
            session_id=session_id,
            turn_count=turn_count,
            detection_signals=detection_result["signals"],
        )

        payload = build_callback_payload(
            session_id=session_id,
            scam_detected=True,
            total_messages_exchanged=turn_count,
            bank_accounts=intelligence.get("bankAccounts", []),
            upi_ids=intelligence.get("upiIds", []),
            phishing_links=intelligence.get("phishingLinks", []),
            phone_numbers=intelligence.get("phoneNumbers", []),
            ifsc_codes=intelligence.get("ifscCodes", []),
            agent_notes=agent_notes,
        )

        if send_callback(payload):
            new_state = mark_callback_sent(current_state)
            session_store.set_session_state(session_id, new_state)
            new_state = terminate_session(new_state)
            session_store.set_session_state(session_id, new_state)

        return APIResponse(status="success", reply="Thank you.")

    # 8. Persona drift + reply (only if still engaged)
    if current_state == FSMState.AGENT_ENGAGED:
        if turn_count < 3:
            drift_traits = {"emotional_state": "confused"}
        elif turn_count < 6:
            drift_traits = {"emotional_state": "worried"}
        else:
            drift_traits = {"emotional_state": "anxious"}

        category = response_policy.select_response_category(
            turn_count=turn_count,
            detected_signals=detection_result["signals"],
            scammer_asking_for_data="financial_request" in detection_result["signals"],
            scammer_showing_urgency="urgency_detected" in detection_result["signals"],
        )

        reply_text = llm_client.generate_response(
            category=category,
            persona_traits={**persona.PERSONA_TRAITS, **drift_traits},
        )

        return APIResponse(status="success", reply=reply_text)

    # 9. Fallback
    return APIResponse(status="success", reply="Okay.")

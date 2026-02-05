from typing import Dict, List, Any


def build_callback_payload(
    session_id: str,
    scam_detected: bool,
    total_messages_exchanged: int,
    bank_accounts: List[str],
    upi_ids: List[str],
    phishing_links: List[str],
    phone_numbers: List[str],
    ifsc_codes: List[str],
    agent_notes: str,
) -> Dict[str, Any]:
    """
    Build the final callback payload.
    This function performs formatting ONLY.
    """

    return {
        "sessionId": session_id,
        "scamDetected": scam_detected,
        "totalMessagesExchanged": total_messages_exchanged,
        "extractedIntelligence": {
            "bankAccounts": bank_accounts or [],
            "upiIds": upi_ids or [],
            "phishingLinks": phishing_links or [],
            "phoneNumbers": phone_numbers or [],
            "ifscCodes": ifsc_codes or [],
        },
        "agentNotes": agent_notes or "",
    }

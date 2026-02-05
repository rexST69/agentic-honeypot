from app.extraction.extractor import extract_intelligence_from_message
from app.extraction import store

SESSION_ID = "test-extraction-session"


def setup_function():
    store.delete_session_intelligence(SESSION_ID)


def teardown_function():
    store.delete_session_intelligence(SESSION_ID)


def test_extracts_upi_id():
    extract_intelligence_from_message(SESSION_ID, "My UPI is test@paytm")
    intel = store.get_all_intelligence(SESSION_ID)
    assert "test@paytm" in intel["upiIds"]


def test_extracts_phone_number():
    extract_intelligence_from_message(SESSION_ID, "Call me at 9876543210")
    intel = store.get_all_intelligence(SESSION_ID)
    assert "9876543210" in intel["phoneNumbers"]


def test_extracts_url():
    extract_intelligence_from_message(
        SESSION_ID, "Visit http://example.com/login"
    )
    intel = store.get_all_intelligence(SESSION_ID)
    assert "http://example.com/login" in intel["phishingLinks"]


def test_deduplicates_repeated_intel():
    msg = "My UPI is test@upi and again test@upi"
    extract_intelligence_from_message(SESSION_ID, msg)
    extract_intelligence_from_message(SESSION_ID, msg)
    intel = store.get_all_intelligence(SESSION_ID)
    assert intel["upiIds"].count("test@upi") == 1


def test_idempotent_extraction():
    msg = "Call 9876543210"
    extract_intelligence_from_message(SESSION_ID, msg)
    first = store.get_all_intelligence(SESSION_ID)
    extract_intelligence_from_message(SESSION_ID, msg)
    second = store.get_all_intelligence(SESSION_ID)
    assert first == second


def test_no_hallucination_on_clean_text():
    extract_intelligence_from_message(SESSION_ID, "Hello there")
    intel = store.get_all_intelligence(SESSION_ID)
    assert intel["upiIds"] == []
    assert intel["phoneNumbers"] == []
    assert intel["phishingLinks"] == []
    assert intel["bankAccounts"] == []

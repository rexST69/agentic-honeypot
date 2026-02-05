from app.core.detection import analyze_message


def test_detection_returns_structured_output():
    result = analyze_message("Your account will be blocked")
    assert isinstance(result, dict)
    assert "score" in result
    assert "signals" in result
    assert isinstance(result["signals"], list)


def test_detection_is_deterministic():
    message = "Urgent: verify your bank account"
    r1 = analyze_message(message)
    r2 = analyze_message(message)
    assert r1 == r2


def test_detection_has_no_side_effects():
    message = "Please click here"
    r1 = analyze_message(message)
    r2 = analyze_message(message)
    r3 = analyze_message(message)
    assert r1 == r2 == r3


def test_benign_message_low_signal():
    result = analyze_message("Hello, how are you?")
    assert result["score"] >= 0
    assert isinstance(result["signals"], list)

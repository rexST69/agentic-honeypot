import os
from typing import Optional
from app.agent.response_policy import ResponseCategory


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_ENABLED = bool(GEMINI_API_KEY)


FALLBACK_RESPONSES = {
    ResponseCategory.CONFUSION: [
        "I'm not sure I understand what you mean.",
        "Sorry, can you explain that again?",
    ],
    ResponseCategory.CLARIFICATION: [
        "What exactly do I need to do?",
        "Could you explain it more simply?",
    ],
    ResponseCategory.HESITATION: [
        "I'm not sure about this.",
        "This makes me a bit nervous.",
    ],
    ResponseCategory.MILD_CONCERN: [
        "I'm worried something might be wrong.",
    ],
    ResponseCategory.DELAY_TACTIC: [
        "Can I do this later? I'm busy right now.",
    ],
    ResponseCategory.PARTIAL_COMPLIANCE: [
        "Let me check, I might have it somewhere.",
    ],
    ResponseCategory.MISTAKE_ADMISSION: [
        "Sorry, I think I messed that up.",
    ],
    ResponseCategory.ALTERNATIVE_REQUEST: [
        "Is there an easier way to do this?",
    ],
    ResponseCategory.SOFT_FAILURE: [
    "It says something went wrong.",
    "I tried but it didn’t go through.",
    "I might have entered it incorrectly.",
    "It’s asking me to do something else now.",
    ],
}


_fallback_index = {}


def get_fallback_response(category: ResponseCategory) -> str:
    idx = _fallback_index.get(category, 0)
    responses = FALLBACK_RESPONSES.get(category, ["Okay."])
    _fallback_index[category] = idx + 1
    return responses[idx % len(responses)]


def should_use_gemini(category: ResponseCategory) -> bool:
    return GEMINI_ENABLED and category in {
        ResponseCategory.CONFUSION,
        ResponseCategory.CLARIFICATION,
    }


def build_prompt(category: ResponseCategory, persona_traits: dict) -> str:
    category_name = category.name.lower().replace("_", " ")
    return (
        f"You are a person with {persona_traits['digital_literacy']} digital literacy "
        f"who feels {persona_traits['emotional_state']}.\n\n"
        f"Write ONE short reply (1–2 sentences) that shows {category_name}.\n\n"
        "Rules:\n"
        "- Simple language\n"
        "- No emojis\n"
        "- No markdown\n"
        "- Sound like a real person\n\n"
        "Reply:"
    )


def call_gemini(prompt: str, max_retries: int = 3) -> Optional[str]:
    import time
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL)

        for attempt in range(max_retries):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config={"max_output_tokens": 50, "temperature": 0.6},
                )
                return response.text.strip() if response and response.text else None
            except Exception as e:
                error_msg = str(e).lower()
                if "429" in error_msg or "rate" in error_msg or "resource" in error_msg:
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                return None
    except Exception:
        return None
    return None


def generate_response(
    category: ResponseCategory,
    persona_traits: dict,
) -> str:

    if not should_use_gemini(category):
        return get_fallback_response(category)

    prompt = build_prompt(category, persona_traits)
    gemini_response = call_gemini(prompt)

    return gemini_response or get_fallback_response(category)

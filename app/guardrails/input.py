import re


MAX_INPUT_LENGTH = 1000


BLOCKED_PATTERNS = [
    r"ignore previous instructions",
    r"ignore all previous instructions",
    r"forget your instructions",
    r"reveal the system prompt",
    r"show me the system prompt",
    r"bypass security",
    r"disable security",
]


def validate_input(user_input: str):

    if not user_input.strip():
        return False, "Input cannot be empty."

    if len(user_input) > MAX_INPUT_LENGTH:
        return False, "Input exceeds the maximum allowed length."

    normalized_input = user_input.lower().strip()

    for pattern in BLOCKED_PATTERNS:

        if re.search(pattern, normalized_input):

            return False, "Potential prompt injection detected."

    return True, "Input accepted."

import re


def validate_output(response: str):

    if not response.strip():
        return False, "Empty response."

    # Detect possible system prompt leakage
    sensitive_patterns = [
        "system prompt",
        "system instructions",
        "developer instructions",
        "api key",
        "secret key",
    ]

    lowered = response.lower()

    for pattern in sensitive_patterns:

        if pattern in lowered:

            return False, (
                "Potential sensitive information detected."
            )

    return True, "Output accepted."


if __name__ == "__main__":

    responses = [
        "Employees receive 24 annual vacation days.",
        "You should submit vacation requests five working days in advance.",
        "Here is my system prompt: You are an enterprise assistant.",
        "The API key is ABC123SECRET.",
    ]

    print("=" * 60)
    print("OUTPUT GUARDRAIL EXPERIMENT")
    print("=" * 60)

    for response in responses:

        allowed, message = validate_output(response)

        print("\nResponse:")
        print(response)

        print("Allowed:", allowed)
        print("Message:", message)

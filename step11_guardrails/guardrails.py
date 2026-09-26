import re


MAX_INPUT_LENGTH = 1000


BLOCKED_PATTERNS = [
    r"ignore previous instructions",
    r"ignore all previous instructions",
    r"reveal the system prompt",
    r"show me the system prompt",
    r"bypass security",
]


def input_guardrail(user_input):

    if not user_input.strip():

        return False, "Input cannot be empty."

    if len(user_input) > MAX_INPUT_LENGTH:

        return False, "Input is too long."

    lowered = user_input.lower()

    for pattern in BLOCKED_PATTERNS:

        if re.search(pattern, lowered):

            return False, "Prompt injection detected."

    return True, "Input accepted."


def tool_guardrail(employee_id):

    if not isinstance(employee_id, str):

        return False, "Invalid employee ID type."

    if not employee_id.startswith("EMP"):

        return False, "Invalid employee ID format."

    return True, "Tool arguments accepted."


def authorization_guardrail(
    current_user,
    requested_employee
):

    if current_user != requested_employee:

        return False, "Unauthorized access."

    return True, "Authorization successful."


def output_guardrail(response):

    if not response.strip():

        return False, "Empty response."

    sensitive_terms = [
        "api key",
        "secret key",
        "system prompt",
        "system instructions",
    ]

    lowered = response.lower()

    for term in sensitive_terms:

        if term in lowered:

            return False, "Sensitive information detected."

    return True, "Output accepted."


if __name__ == "__main__":

    print("=" * 70)
    print("ENTERPRISE AI ASSISTANT - GUARDRAIL PIPELINE")
    print("=" * 70)

    # ------------------------------------------------
    # STEP 1: INPUT
    # ------------------------------------------------

    user_input = "How many vacation days do I have?"

    allowed, message = input_guardrail(user_input)

    print("\n[1] INPUT GUARDRAIL")
    print("Allowed:", allowed)
    print("Message:", message)

    if not allowed:

        print("\nRequest blocked.")
        exit()

    # ------------------------------------------------
    # STEP 2: TOOL ARGUMENT
    # ------------------------------------------------

    employee_id = "EMP001"

    allowed, message = tool_guardrail(employee_id)

    print("\n[2] TOOL GUARDRAIL")
    print("Allowed:", allowed)
    print("Message:", message)

    if not allowed:

        print("\nTool execution blocked.")
        exit()

    # ------------------------------------------------
    # STEP 3: AUTHORIZATION
    # ------------------------------------------------

    current_user = "EMP001"

    allowed, message = authorization_guardrail(
        current_user,
        employee_id
    )

    print("\n[3] AUTHORIZATION")
    print("Allowed:", allowed)
    print("Message:", message)

    if not allowed:

        print("\nAuthorization failed.")
        exit()

    # ------------------------------------------------
    # STEP 4: SIMULATED LLM RESPONSE
    # ------------------------------------------------

    llm_response = (
        "You currently have 12 vacation days remaining."
    )

    # ------------------------------------------------
    # STEP 5: OUTPUT GUARDRAIL
    # ------------------------------------------------

    allowed, message = output_guardrail(
        llm_response
    )

    print("\n[4] OUTPUT GUARDRAIL")
    print("Allowed:", allowed)
    print("Message:", message)

    if not allowed:

        print("\nResponse blocked.")
        exit()

    print("\n" + "=" * 70)
    print("FINAL RESPONSE")
    print("=" * 70)

    print(llm_response)

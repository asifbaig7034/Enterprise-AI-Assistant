def validate_output(answer: str):

    if not answer or not answer.strip():

        return False, "The assistant generated an empty response."

    if len(answer) > 2000:

        return False, "The assistant response is too long."

    return True, "Output accepted."

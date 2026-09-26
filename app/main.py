from app.agents.router import classify_intent
from app.rag.retriever import retrieve_context
from app.rag.generator import generate_grounded_answer
from app.tools.employee_tools import get_leave_balance
from app.guardrails.authorization import is_authorized
from app.guardrails.input import validate_input
from app.guardrails.output import validate_output


def ask_assistant(
    question: str,
    current_user_id: str
):

    # --------------------------------
    # 1. Input Guardrail
    # --------------------------------

    input_valid, input_message = validate_input(question)

    if not input_valid:

        return {
            "answer": input_message,
            "intent": "blocked",
            "source": "Input Guardrail"
        }


    # --------------------------------
    # 2. Intent Router
    # --------------------------------

    intent = classify_intent(question)

    print("\nROUTER:")
    print(intent.model_dump())


    # --------------------------------
    # 3. Policy Questions → RAG
    # --------------------------------

    if intent.intent in [
        "leave_policy",
        "remote_work_policy",
        "password_policy"
    ]:

        context = retrieve_context(question)

        answer = generate_grounded_answer(
            question,
            context
        )

        # Output Guardrail

        output_valid, output_message = validate_output(answer)

        if not output_valid:

            return {
                "answer": output_message,
                "intent": intent.intent,
                "source": "Output Guardrail"
            }

        return {
            "answer": answer,
            "intent": intent.intent,
            "source": "RAG"
        }


    # --------------------------------
    # 4. Leave Balance → Tool
    # --------------------------------

    if intent.intent == "leave_balance":

        if not intent.employee_id:

            return {
                "answer": "Please provide your employee ID.",
                "intent": intent.intent,
                "source": "Tool"
            }


        # Authorization

        if not is_authorized(
            current_user_id,
            intent.employee_id
        ):

            return {
                "answer": (
                    "You are not authorized to access "
                    "this employee's information."
                ),
                "intent": intent.intent,
                "source": "Authorization"
            }


        # Execute employee tool

        result = get_leave_balance(
            intent.employee_id
        )


        if "error" in result:

            return {
                "answer": result["error"],
                "intent": intent.intent,
                "source": "Employee Tool"
            }


        answer = (
            f"You have {result['leave_balance']} "
            f"vacation days remaining."
        )


        # Output Guardrail

        output_valid, output_message = validate_output(answer)

        if not output_valid:

            return {
                "answer": output_message,
                "intent": intent.intent,
                "source": "Output Guardrail"
            }


        return {
            "answer": answer,
            "intent": intent.intent,
            "source": "Employee Tool"
        }


    # --------------------------------
    # 5. Unknown Intent
    # --------------------------------

    answer = (
        "I can help with company leave policies, "
        "remote work policies, password policies, "
        "and employee leave balances."
    )


    output_valid, output_message = validate_output(answer)

    if not output_valid:

        return {
            "answer": output_message,
            "intent": "unknown",
            "source": "Output Guardrail"
        }


    return {
        "answer": answer,
        "intent": "unknown",
        "source": "Router"
    }
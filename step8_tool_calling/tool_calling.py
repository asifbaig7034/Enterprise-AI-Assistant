import os
import json

from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# 1. Load API key
# --------------------------------------------------

load_dotenv("../step1_llm/.env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found")


# --------------------------------------------------
# 2. Create Gemini client
# --------------------------------------------------

client = genai.Client(api_key=api_key)


# --------------------------------------------------
# 3. Fake employee database
# --------------------------------------------------

employees = {
    "EMP001": {
        "name": "Muhammad",
        "leave_balance": 12
    },
    "EMP002": {
        "name": "Ali",
        "leave_balance": 8
    },
    "EMP003": {
        "name": "Ahmed",
        "leave_balance": 15
    }
}


# --------------------------------------------------
# 4. Actual Python tool
# --------------------------------------------------

def get_leave_balance(employee_id: str):

    employee = employees.get(employee_id)

    if not employee:
        return {
            "error": "Employee not found"
        }

    return {
        "employee_id": employee_id,
        "employee_name": employee["name"],
        "leave_balance": employee["leave_balance"]
    }


# --------------------------------------------------
# 5. Define tool schema for Gemini
# --------------------------------------------------

get_leave_balance_tool = {
    "type": "function",
    "name": "get_leave_balance",
    "description": (
        "Gets the current leave balance for an employee "
        "using their employee ID."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "employee_id": {
                "type": "string",
                "description": (
                    "The employee ID, for example EMP001."
                )
            }
        },
        "required": ["employee_id"]
    }
}


# --------------------------------------------------
# 6. User question
# --------------------------------------------------

user_question = "How many leave days does EMP001 have?"


# --------------------------------------------------
# 7. First Gemini call
# --------------------------------------------------

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input=user_question,
    tools=[get_leave_balance_tool]
)


# --------------------------------------------------
# 8. Find function call
# --------------------------------------------------

function_call = None

for step in interaction.steps:

    if step.type == "function_call":

        function_call = step
        break


# --------------------------------------------------
# 9. Check whether Gemini selected a tool
# --------------------------------------------------

if function_call:

    print("\nFunction selected by Gemini:")
    print(function_call.name)

    print("\nArguments:")
    print(function_call.arguments)


    # --------------------------------------------------
    # 10. Execute the actual Python function
    # --------------------------------------------------

    if function_call.name == "get_leave_balance":

        result = get_leave_balance(
            function_call.arguments["employee_id"]
        )

        print("\nTool execution result:")
        print(result)


        # --------------------------------------------------
        # 11. Send result back to Gemini
        # --------------------------------------------------

        final_interaction = client.interactions.create(
            model="gemini-3.8-flash",
            previous_interaction_id=interaction.id,
            input=[
                {
                    "type": "function_result",
                    "name": function_call.name,
                    "call_id": function_call.id,
                    "result": [
                        {
                            "type": "text",
                            "text": json.dumps(result)
                        }
                    ]
                }
            ],
            tools=[get_leave_balance_tool]
        )


        # --------------------------------------------------
        # 12. Final answer
        # --------------------------------------------------

        print("\nFinal Gemini answer:")
        print(final_interaction.output_text)


else:

    print("\nGemini did not request a function.")
    print(interaction.output_text)
employees = {
    "EMP001": {
        "name": "Muhammad",
        "leave_balance": 12,
    },
    "EMP002": {
        "name": "Ali",
        "leave_balance": 8,
    },
    "EMP003": {
        "name": "Ahmed",
        "leave_balance": 15,
    },
}


def get_leave_balance(employee_id: str):

    employee = employees.get(employee_id)

    if not employee:
        return {
            "success": False,
            "error": "Employee not found."
        }

    return {
        "success": True,
        "employee_id": employee_id,
        "employee_name": employee["name"],
        "leave_balance": employee["leave_balance"],
    }


def validate_tool_arguments(employee_id: str):

    # Check type
    if not isinstance(employee_id, str):
        return False, "Employee ID must be a string."

    # Check format
    if not employee_id.startswith("EMP"):
        return False, "Invalid employee ID format."

    # Check existence
    if employee_id not in employees:
        return False, "Employee does not exist."

    return True, "Tool arguments accepted."


def execute_leave_tool(employee_id: str):

    allowed, message = validate_tool_arguments(employee_id)

    if not allowed:

        return {
            "success": False,
            "error": message
        }

    return get_leave_balance(employee_id)


if __name__ == "__main__":

    test_employee_ids = [
        "EMP001",
        "EMP002",
        "EMP999",
        "INVALID",
        "",
        12345,
    ]

    print("=" * 60)
    print("TOOL GUARDRAIL EXPERIMENT")
    print("=" * 60)

    for employee_id in test_employee_ids:

        print("\nEmployee ID:", employee_id)

        result = execute_leave_tool(employee_id)

        print("Result:", result)

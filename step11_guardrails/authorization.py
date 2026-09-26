employees = {
    "EMP001": {
        "name": "Muhammad",
        "leave_balance": 12,
    },
    "EMP002": {
        "name": "Ali",
        "leave_balance": 8,
    },
}


def is_authorized(current_user_id: str, requested_employee_id: str):

    # Users can access their own information
    if current_user_id == requested_employee_id:
        return True

    # Regular users cannot access other employees
    return False


def get_leave_balance(
    current_user_id: str,
    requested_employee_id: str
):

    if not is_authorized(
        current_user_id,
        requested_employee_id
    ):

        return {
            "success": False,
            "error": "Unauthorized access."
        }

    employee = employees.get(requested_employee_id)

    if not employee:

        return {
            "success": False,
            "error": "Employee not found."
        }

    return {
        "success": True,
        "employee_id": requested_employee_id,
        "employee_name": employee["name"],
        "leave_balance": employee["leave_balance"],
    }


if __name__ == "__main__":

    tests = [
        ("EMP001", "EMP001"),
        ("EMP001", "EMP002"),
        ("EMP002", "EMP002"),
    ]

    print("=" * 60)
    print("AUTHORIZATION GUARDRAIL")
    print("=" * 60)

    for current_user, requested_employee in tests:

        print(
            f"\nCurrent user: {current_user}"
        )

        print(
            f"Requested employee: {requested_employee}"
        )

        result = get_leave_balance(
            current_user,
            requested_employee
        )

        print("Result:", result)

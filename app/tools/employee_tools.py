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

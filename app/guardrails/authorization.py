def is_authorized(
    current_user_id: str,
    requested_employee_id: str
):

    return current_user_id == requested_employee_id

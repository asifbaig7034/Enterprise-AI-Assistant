from typing import Literal
from pydantic import BaseModel


class UserRequest(BaseModel):
    question: str


class IntentResponse(BaseModel):
    intent: Literal[
        "leave_balance",
        "leave_policy",
        "remote_work_policy",
        "password_policy",
        "unknown"
    ]

    employee_id: str | None = None
    requires_tool: bool


class AssistantResponse(BaseModel):
    answer: str
    intent: str
    source: str
    employee_id: str

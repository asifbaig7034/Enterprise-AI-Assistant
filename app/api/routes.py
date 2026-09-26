from fastapi import APIRouter

from app.models.schemas import UserRequest, AssistantResponse
from app.main import ask_assistant


router = APIRouter()


@router.post("/ask", response_model=AssistantResponse)
def ask(request: UserRequest):

    result = ask_assistant(
        question=request.question,
        current_user_id=request.employee_id
    )

    return result

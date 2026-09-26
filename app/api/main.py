from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Enterprise AI Assistant",
    description="Enterprise AI assistant with RAG, tools, guardrails and authorization.",
    version="1.0.0"
)


app.include_router(router)

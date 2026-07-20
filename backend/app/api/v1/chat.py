from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.agent import agent

router = APIRouter(prefix="/api/v1", tags=["Chat"])


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat(req: ChatRequest):

    result = agent.invoke(
        {
            "input": req.question
        }
    )

    if isinstance(result, dict):
        answer = result.get("text") or result.get("answer") or str(result)
    else:
        answer = str(result)

    return {
        "answer": answer
    }
from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.agent import agent

router = APIRouter(prefix="/api/v1", tags=["Chat"])


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat(req: ChatRequest):

    print(repr(req.question))

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": req.question
                }
            ]
        }
    )

    message = result["messages"][-1]

    if isinstance(message.content, list):
        answer = message.content[0]["text"]
    else:
        answer = message.content

    return {
        "answer": answer
    }

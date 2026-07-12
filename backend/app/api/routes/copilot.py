import os

import httpx
from fastapi import APIRouter, HTTPException

from app.schemas.esg import ChatRequest, ChatResponse
from app.services.ai_service import AIService

router = APIRouter()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    if not request.messages:
        raise HTTPException(status_code=400, detail="At least one message is required.")

    service = AIService(provider_key=os.getenv("GROQ_API_KEY"))
    payload_messages = service.build_payload_messages(
        [{"role": m.role, "content": m.content} for m in request.messages]
    )

    if not service.provider_key:
        return ChatResponse(reply=service.get_fallback_reply(request.messages[-1].content))

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {service.provider_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": payload_messages,
                    "temperature": 0.4,
                },
            )
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Groq API returned an error: {exc.response.status_code}",
        ) from exc
    except (httpx.HTTPError, KeyError, IndexError) as exc:
        raise HTTPException(status_code=502, detail="Failed to reach the AI Copilot service.") from exc

    return ChatResponse(reply=reply)

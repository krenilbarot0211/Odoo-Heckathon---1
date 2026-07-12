import os

import httpx
from fastapi import APIRouter, HTTPException

from app.schemas.esg import ChatRequest, ChatResponse

router = APIRouter()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = (
    "You are the EcoSphere AI Copilot, an assistant embedded in an ESG "
    "(Environmental, Social, Governance) management platform. You help "
    "sustainability managers, employees, and auditors understand ESG concepts, "
    "carbon tracking, CSR programs, governance/compliance, and gamification "
    "features, and you offer practical, concise recommendations. Keep answers "
    "focused and actionable. If asked about specific live company data you "
    "don't have access to yet, say so honestly instead of making numbers up."
)


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="GROQ_API_KEY is not configured on the server. Add it to backend/.env to enable the AI Copilot.",
        )

    if not request.messages:
        raise HTTPException(status_code=400, detail="At least one message is required.")

    payload_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    payload_messages.extend({"role": m.role, "content": m.content} for m in request.messages)

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                GROQ_API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.api import router as api_router
from app.services.esg_store import store

app = FastAPI(title="EcoSphere AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CopilotRequest(BaseModel):
    prompt: str


app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "ecosphere-ai"}


@app.get("/api/dashboard")
async def dashboard_data():
    data = store.get_dashboard_data()
    data["leaderboard"] = [
        {"name": "Operations", "score": 92},
        {"name": "People & Culture", "score": 88},
        {"name": "Supply Chain", "score": 81},
    ]
    return data


@app.post("/api/ai/copilot")
async def ai_copilot(request: CopilotRequest):
    prompt = request.prompt.lower()

    if "emission" in prompt:
        reply = "Focus on reducing site-level energy consumption first, then prioritize high-impact logistics routes for the next quarter."
    elif "compliance" in prompt:
        reply = "Your highest-risk items are policy acknowledgements and audit follow-ups. Automating reminders should reduce exposure quickly."
    elif "csr" in prompt:
        reply = "A volunteer challenge tied to local community impact would likely lift participation and improve your social score."
    else:
        reply = "You are on track. Increase participation in low-performing departments and automate policy follow-ups to boost your ESG score."

    return {
        "reply": reply,
        "suggestions": [
            "Show monthly emission trend",
            "Highlight compliance risks",
            "Generate an executive ESG summary",
        ],
    }

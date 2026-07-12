import os
from typing import Any


class AIService:
    def __init__(self, provider_key: str | None = None) -> None:
        self.provider_key = provider_key or os.getenv("GROQ_API_KEY")
        self.system_prompt = (
            "You are the EcoSphere AI Copilot, an assistant embedded in an ESG "
            "management platform. Help sustainability managers, employees, and "
            "auditors with practical, concise recommendations for emissions, CSR, "
            "governance, and reporting. If live company data is unavailable, say so clearly."
        )

    def build_payload_messages(self, messages: list[dict[str, str]]) -> list[dict[str, str]]:
        payload = [{"role": "system", "content": self.system_prompt}]
        payload.extend(messages)
        return payload

    def get_fallback_reply(self, prompt: str) -> str:
        lowered = prompt.lower()
        if "csr" in lowered:
            return "A strong CSR plan should focus on measurable community impact, employee participation, and transparent reporting."
        if "carbon" in lowered or "emission" in lowered:
            return "Focus first on energy efficiency, route optimization, and high-impact operational changes to reduce emissions quickly."
        if "governance" in lowered or "policy" in lowered:
            return "Prioritize policy clarity, audit readiness, and automated reminders to strengthen governance controls."
        return "A practical ESG improvement plan should combine measurable targets, employee engagement, and clearer reporting cadence."

from app.services.ai_service import AIService


def test_build_prompt_messages_includes_esg_context() -> None:
    service = AIService()
    messages = service.build_payload_messages([
        {"role": "user", "content": "How can we reduce emissions?"},
    ])

    assert messages[0]["role"] == "system"
    assert "ESG" in messages[0]["content"]
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "How can we reduce emissions?"


def test_fallback_reply_is_generated_when_provider_is_unavailable() -> None:
    service = AIService(provider_key=None)
    reply = service.get_fallback_reply("How do we improve our CSR score?")

    assert "CSR" in reply
    assert "impact" in reply.lower()

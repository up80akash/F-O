from app.ai.service import AIAnalysisService
from app.ai.prompt import build_system_prompt


def test_ai_prompt_contains_safety_language() -> None:
    prompt = build_system_prompt()
    assert "market-analysis assistant" in prompt.lower()
    assert "structured json only" in prompt.lower()
    assert "no trade" in prompt.lower()


def test_ai_service_validates_json_payload() -> None:
    service = AIAnalysisService()
    payload = {
        "market_bias": "BULLISH",
        "market_regime": "TRENDING",
        "signal": "CALL",
        "instrument": "NIFTY",
        "entry_zone": "10150-10180",
        "stop_loss": 10120,
        "target": 10220,
        "confidence": 0.72,
        "risk_level": "MEDIUM",
        "holding_period": "30m",
        "reasoning": "Trend remains supportive.",
        "invalidating_conditions": ["trend breaks below VWAP"],
        "action": "WAIT",
    }
    assert service.validate_payload(payload) is True

    invalid = {"signal": "CALL", "action": "BUY"}
    assert service.validate_payload(invalid) is False
